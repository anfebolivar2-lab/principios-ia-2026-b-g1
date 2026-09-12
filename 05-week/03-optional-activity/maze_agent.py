"""
maze_agent.py
=============

PLANTILLA DE ESTUDIO para el parcial practico "Implementacion de agente
de busqueda" (laberinto, BFS vs A*, 80 minutos, individual).

En el examen te daran el laberinto ya armado (como dict o como lista de
listas). Este archivo esta pensado para que, llegado el momento, solo
tengas que:

    1. Pegar el laberinto que te entreguen en MAZE (o adaptar `normalize_maze`
       si viene en un formato distinto al de aqui).
    2. Ajustar START y GOAL si no coinciden con los que te dan.
    3. Ejecutar el archivo: ya imprime todo lo que pide la rubrica.

Corre de una vez con un laberinto de ejemplo para que puedas practicar y
verificar que el flujo completo funciona.
"""

from collections import deque
import heapq
import itertools


# ===========================================================================
# 0. FORMULACION DEL PROBLEMA COMO ESPACIO DE ESTADOS  (punto de la rubrica)
# ===========================================================================
#
#   Estados:            cada celda transitable (fila, columna) del laberinto.
#   Estado inicial:     la celda START = (fila_inicio, col_inicio).
#   Estado objetivo:    la celda GOAL = (fila_meta, col_meta).
#   Acciones:           moverse "arriba", "abajo", "izquierda" o "derecha"
#                        desde la celda actual.
#   Modelo de transicion: A(estado, accion) -> celda vecina en la direccion
#                        de la accion, SOLO SI esa celda esta dentro de la
#                        grilla y no es una pared (valor 1 / '#').
#   Costo de camino:    cada movimiento cuesta 1 (costo uniforme), por lo
#                        que el costo total de una solucion es su numero de
#                        pasos.
#   Test de objetivo:   estado_actual == GOAL.
#
# (Estos son los 5 componentes que pide la rubrica: estados, estado inicial,
#  acciones/modelo de transicion, costo de camino y test de objetivo.)


# ===========================================================================
# 1. ENTRADA: laberinto de ejemplo (reemplazar por el del examen)
# ===========================================================================

# Formato lista de listas: 0 = libre, 1 = pared.
MAZE = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]

START = (0, 0)
GOAL = (4, 4)


def normalize_maze(maze):
    """
    Acepta el laberinto en cualquiera de los dos formatos que puede dar el
    profesor y lo deja siempre como una lista de listas de 0/1:

      (a) Lista de listas ya (se devuelve tal cual).
      (b) Dict con llaves (fila, columna) -> valor, p. ej.
          {(0, 0): 0, (0, 1): 1, ...}. Se infiere el tamano de la grilla a
          partir de las llaves y se rellena una matriz.

    Ajusta esta funcion en el examen si el formato entregado es distinto
    (por ejemplo, paredes como '#' y libre como '.').
    """
    if isinstance(maze, dict):
        max_row = max(r for r, _ in maze) + 1
        max_col = max(c for _, c in maze) + 1
        grid = [[1] * max_col for _ in range(max_row)]
        for (r, c), value in maze.items():
            grid[r][c] = value
        return grid
    return maze


def is_wall(value) -> bool:
    """Centraliza que cuenta como 'pared'. Ajustar si usan '#'/'.' en vez de 1/0."""
    return value == 1 or value == "#"


# ===========================================================================
# 2. MODELO DE SUCESORES Y HEURISTICA
# ===========================================================================

MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha


def successors(state, grid):
    """Vecinos validos (dentro de la grilla y sin pared) de una celda."""
    rows, cols = len(grid), len(grid[0])
    r, c = state
    result = []
    for dr, dc in MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and not is_wall(grid[nr][nc]):
            result.append((nr, nc))
    return result


def manhattan(a, b):
    """h(n): distancia Manhattan entre la celda actual y la meta.
    Es admisible porque, sin paredes, el minimo numero de pasos entre dos
    celdas de una grilla en la que solo se puede mover en 4 direcciones es
    exactamente |dr| + |dc|; con paredes el camino real solo puede ser igual
    o mas largo, nunca mas corto, asi que h nunca sobreestima."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ===========================================================================
# 3. BFS
# ===========================================================================

def bfs(grid, start, goal):
    if start == goal:
        return [start], 0

    frontier = deque([start])
    came_from = {start: None}
    nodes_expanded = 0

    while frontier:
        node = frontier.popleft()
        nodes_expanded += 1

        for neighbor in successors(node, grid):
            if neighbor not in came_from:
                came_from[neighbor] = node
                if neighbor == goal:
                    return _reconstruct(came_from, start, goal), nodes_expanded
                frontier.append(neighbor)

    return None, nodes_expanded  # sin solucion


# ===========================================================================
# 4. A* con heuristica Manhattan
# ===========================================================================

def astar(grid, start, goal):
    if start == goal:
        return [start], 0

    counter = itertools.count()  # desempate estable en el heap
    frontier = [(manhattan(start, goal), next(counter), start)]
    came_from = {start: None}
    g_score = {start: 0}
    nodes_expanded = 0
    visited = set()

    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node in visited:
            continue
        visited.add(node)
        nodes_expanded += 1

        if node == goal:
            return _reconstruct(came_from, start, goal), nodes_expanded

        for neighbor in successors(node, grid):
            tentative_g = g_score[node] + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                came_from[neighbor] = node
                f = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(frontier, (f, next(counter), neighbor))

    return None, nodes_expanded  # sin solucion


def _reconstruct(came_from, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


# ===========================================================================
# 5. MAIN: imprime camino, nodos expandidos y cual fue mas eficiente
# ===========================================================================

if __name__ == "__main__":
    grid = normalize_maze(MAZE)

    print(f"Inicio: {START}  Meta: {GOAL}\n")

    bfs_path, bfs_nodes = bfs(grid, START, GOAL)
    astar_path, astar_nodes = astar(grid, START, GOAL)

    print("== BFS ==")
    print(f"Camino ({len(bfs_path) - 1} pasos): {bfs_path}")
    print(f"Nodos expandidos: {bfs_nodes}\n")

    print("== A* (heuristica Manhattan) ==")
    print(f"Camino ({len(astar_path) - 1} pasos): {astar_path}")
    print(f"Nodos expandidos: {astar_nodes}\n")

    print("== Comparacion de eficiencia ==")
    if bfs_nodes == astar_nodes:
        print("Ambos algoritmos expandieron el mismo numero de nodos.")
    else:
        mas_eficiente = "A*" if astar_nodes < bfs_nodes else "BFS"
        menos_eficiente = "BFS" if mas_eficiente == "A*" else "A*"
        diferencia = abs(bfs_nodes - astar_nodes)
        print(f"{mas_eficiente} fue mas eficiente: expandio {diferencia} nodos "
              f"menos que {menos_eficiente}.")
        print("Justificacion: BFS expande nodos en orden de cercania al inicio, "
              "sin ninguna nocion de hacia donde queda la meta, por lo que "
              "explora por igual en todas las direcciones. A* usa f(n) = g(n) "
              "+ h(n) con la distancia Manhattan como h(n), lo que prioriza "
              "los nodos que ademas de tener bajo costo acumulado estan mas "
              "cerca de la meta en linea recta, guiando la busqueda hacia el "
              "objetivo en lugar de expandirse a ciegas.")

    assert bfs_path is not None and astar_path is not None, "El laberinto no tiene solucion"
    assert len(bfs_path) == len(astar_path), "BFS y A* deberian encontrar caminos de igual longitud (ambos optimos con costo uniforme)"
