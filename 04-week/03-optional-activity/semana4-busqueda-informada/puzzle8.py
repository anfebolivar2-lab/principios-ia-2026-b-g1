"""
puzzle8.py
==========

Formulacion del problema del 8-puzzle como espacio de estados, y tres
algoritmos de busqueda no informada / informada para resolverlo:

    - Busqueda en anchura (BFS)
    - Busqueda de costo uniforme (UCS)
    - A* con heuristica de distancia Manhattan

Representacion del estado
--------------------------
Un estado es una tupla de 9 enteros (longitud 9) que representa el
tablero 3x3 leido por filas, de izquierda a derecha y de arriba hacia
abajo. El valor 0 representa el espacio vacio ("blank").

    Indices del tablero (fila, columna):

        0(0,0)  1(0,1)  2(0,2)
        3(1,0)  4(1,1)  5(1,2)
        6(2,0)  7(2,1)  8(2,2)

Estado objetivo (goal): (1, 2, 3, 4, 5, 6, 7, 8, 0)

    1 2 3
    4 5 6
    7 8 _
"""

from __future__ import annotations

import heapq
import itertools
import random
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

State = Tuple[int, ...]

GOAL: State = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Posicion (fila, columna) de cada valor en el estado objetivo, precalculada
# una sola vez para que la heuristica sea O(1) por ficha.
_GOAL_POS: Dict[int, Tuple[int, int]] = {
    value: divmod(index, 3) for index, value in enumerate(GOAL)
}

# Movimientos posibles del espacio vacio en funcion de su posicion en la
# grilla 3x3. Cada movimiento es un delta (dr, dc) y una etiqueta legible.
_MOVES = [(-1, 0, "arriba"), (1, 0, "abajo"), (0, -1, "izquierda"), (0, 1, "derecha")]


# ---------------------------------------------------------------------------
# Modelo del espacio de estados
# ---------------------------------------------------------------------------
#
#   Estados:        las 9!/2 = 181,440 configuraciones alcanzables del
#                    tablero 3x3 (la mitad de las 9! permutaciones posibles,
#                    ya que la paridad de la permutacion se conserva).
#   Estado inicial:  cualquier configuracion del tablero (parametro `start`).
#   Estado objetivo: GOAL, definido arriba (o una funcion goal_test).
#   Acciones:        deslizar el espacio vacio arriba/abajo/izquierda/derecha,
#                    segun no se salga del tablero.
#   Modelo de transicion: swap del 0 con la celda vecina indicada por la
#                    accion -> produce el estado sucesor.
#   Costo de paso:   1 por cada movimiento (costo de camino uniforme).
#   Test de objetivo: state == GOAL.
#
# Esta es la formulacion clasica de Russell & Norvig para el 8-puzzle.


def successors(state: State) -> List[Tuple[State, str]]:
    """Genera los estados sucesores validos y la accion que los produjo."""
    blank = state.index(0)
    row, col = divmod(blank, 3)
    result = []
    for dr, dc, label in _MOVES:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_blank = nr * 3 + nc
            new_state = list(state)
            new_state[blank], new_state[new_blank] = new_state[new_blank], new_state[blank]
            result.append((tuple(new_state), label))
    return result


def manhattan_distance(state: State, goal_pos: Dict[int, Tuple[int, int]] = _GOAL_POS) -> int:
    """
    Heuristica h(n): suma, para cada ficha (sin contar el espacio vacio),
    de la distancia Manhattan entre su posicion actual y su posicion en el
    estado objetivo. Es admisible (nunca sobreestima) porque cada movimiento
    mueve una sola ficha una casilla, y consistente (monotona), por lo que
    A* con esta heuristica es optimo y no reabre nodos ya cerrados.
    """
    total = 0
    for index, value in enumerate(state):
        if value == 0:
            continue
        r, c = divmod(index, 3)
        gr, gc = goal_pos[value]
        total += abs(r - gr) + abs(c - gc)
    return total


def is_solvable(state: State) -> bool:
    """
    Un estado del 8-puzzle es alcanzable desde GOAL si y solo si el numero
    de inversiones (pares fuera de orden, ignorando el 0) es par -- esto
    aplica porque el tablero tiene ancho impar (3 columnas).
    """
    tiles = [v for v in state if v != 0]
    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )
    return inversions % 2 == 0


# ---------------------------------------------------------------------------
# Nodo de busqueda
# ---------------------------------------------------------------------------


@dataclass
class Node:
    state: State
    parent: Optional["Node"]
    action: Optional[str]
    g: int  # costo de camino acumulado desde el estado inicial
    depth: int


def reconstruct_path(node: Node) -> List[str]:
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    return list(reversed(actions))


@dataclass
class SearchResult:
    algorithm: str
    found: bool
    path_length: int
    nodes_expanded: int
    max_frontier_size: int
    time_seconds: float
    actions: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Busqueda genérica por prioridad (usada por UCS y A*)
#
#   UCS  == best_first_search con f(n) = g(n)
#   A*   == best_first_search con f(n) = g(n) + h(n)
#
# ---------------------------------------------------------------------------


def _best_first_search(
    start: State,
    algorithm_name: str,
    heuristic: Callable[[State], int],
) -> SearchResult:
    t0 = time.perf_counter()

    if start == GOAL:
        return SearchResult(algorithm_name, True, 0, 0, 1, time.perf_counter() - t0, [])

    counter = itertools.count()  # desempate estable en el heap
    start_node = Node(start, None, None, 0, 0)
    frontier: List[Tuple[int, int, Node]] = []
    heapq.heappush(frontier, (heuristic(start), next(counter), start_node))
    best_g: Dict[State, int] = {start: 0}
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        _, _, node = heapq.heappop(frontier)

        # Si ya encontramos un camino mejor a este estado, se descarta (lazy deletion).
        if node.g > best_g.get(node.state, float("inf")):
            continue

        if node.state == GOAL:
            elapsed = time.perf_counter() - t0
            return SearchResult(
                algorithm_name, True, node.depth, nodes_expanded,
                max_frontier, elapsed, reconstruct_path(node),
            )

        nodes_expanded += 1
        for child_state, action in successors(node.state):
            g = node.g + 1
            if g < best_g.get(child_state, float("inf")):
                best_g[child_state] = g
                child = Node(child_state, node, action, g, node.depth + 1)
                f = g + heuristic(child_state)
                heapq.heappush(frontier, (f, next(counter), child))

    return SearchResult(algorithm_name, False, -1, nodes_expanded, max_frontier, time.perf_counter() - t0, [])


def astar(start: State) -> SearchResult:
    """A* search: f(n) = g(n) + h(n), h = distancia Manhattan."""
    return _best_first_search(start, "A*", manhattan_distance)


def uniform_cost_search(start: State) -> SearchResult:
    """UCS: f(n) = g(n), equivalente a A* con h(n) = 0."""
    return _best_first_search(start, "UCS", lambda s: 0)


def breadth_first_search(start: State) -> SearchResult:
    """
    BFS explora nivel por nivel. Como el costo de cada paso es 1 (uniforme),
    BFS encuentra el camino optimo igual que UCS, pero usando una cola FIFO
    en lugar de una cola de prioridad.
    """
    t0 = time.perf_counter()

    if start == GOAL:
        return SearchResult("BFS", True, 0, 0, 1, time.perf_counter() - t0, [])

    start_node = Node(start, None, None, 0, 0)
    frontier = deque([start_node])
    visited = {start}
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        node = frontier.popleft()
        nodes_expanded += 1

        for child_state, action in successors(node.state):
            if child_state not in visited:
                child = Node(child_state, node, action, node.g + 1, node.depth + 1)
                if child_state == GOAL:
                    elapsed = time.perf_counter() - t0
                    return SearchResult(
                        "BFS", True, child.depth, nodes_expanded,
                        max_frontier, elapsed, reconstruct_path(child),
                    )
                visited.add(child_state)
                frontier.append(child)

    return SearchResult("BFS", False, -1, nodes_expanded, max_frontier, time.perf_counter() - t0, [])


# ---------------------------------------------------------------------------
# Utilidades para generar instancias de prueba
# ---------------------------------------------------------------------------


def scramble(num_moves: int, seed: int) -> State:
    """
    Genera una instancia inicial aplicando `num_moves` movimientos aleatorios
    validos a partir de GOAL. Esto garantiza que el estado resultante sea
    siempre resoluble (por construccion), y `num_moves` sirve como una cota
    superior aproximada de la dificultad de la instancia.
    """
    rng = random.Random(seed)
    state = GOAL
    last_action = None
    opposite = {"arriba": "abajo", "abajo": "arriba", "izquierda": "derecha", "derecha": "izquierda"}
    for _ in range(num_moves):
        options = [
            (s, a) for s, a in successors(state)
            if a != opposite.get(last_action)
        ]
        state, last_action = rng.choice(options)
    return state


def render(state: State) -> str:
    """Representacion visual en texto de un estado (para depuracion/README)."""
    rows = []
    for r in range(3):
        cells = state[r * 3:(r + 1) * 3]
        rows.append(" ".join(str(c) if c != 0 else "_" for c in cells))
    return "\n".join(rows)
