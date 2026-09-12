# A* vs. BFS vs. Búsqueda de Costo Uniforme — 8-Puzzle

**Autor:** Andrés Felipe Bolívar Arias
**Curso:** Inteligencia Artificial — entrega individual (fork del repositorio de la clase)

Este proyecto implementa el algoritmo **A\*** (con heurística de distancia
Manhattan) para resolver el problema del **8-puzzle**, y lo compara
experimentalmente contra **BFS** (búsqueda en anchura) y **UCS** (búsqueda
de costo uniforme) en 4 instancias de dificultad creciente.

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `puzzle8.py` | Formulación del espacio de estados, generación de sucesores, heurística Manhattan, verificación de solubilidad, e implementación de A*, BFS y UCS. |
| `compare.py` | Corre los tres algoritmos sobre 4 instancias y genera la tabla comparativa (`results.md`). |
| `results.md` | Salida cruda de la última ejecución de `compare.py` (se regenera automáticamente). |
| `README.md` | Este informe. |

Para reproducir los resultados:

```bash
python3 compare.py
```

No requiere dependencias externas (solo la librería estándar de Python 3).

---

## 1. Formulación del problema como espacio de estados

El 8-puzzle se modela como un problema de búsqueda clásico (formulación de
Russell & Norvig):

- **Estado:** una configuración del tablero 3×3, representada como una
  tupla de 9 enteros leída por filas. El valor `0` representa el espacio
  vacío ("blank"). Ejemplo:

  ```
  1 2 3
  4 _ 6      ->  (1, 2, 3, 4, 0, 6, 7, 5, 8)
  7 5 8
  ```

- **Estado inicial:** cualquier configuración del tablero, generada
  aleatoriamente a partir del objetivo aplicando N movimientos válidos
  (esto garantiza que la instancia sea siempre soluble).

- **Estado objetivo:** `(1, 2, 3, 4, 5, 6, 7, 8, 0)`, es decir:

  ```
  1 2 3
  4 5 6
  7 8 _
  ```

- **Acciones:** deslizar el espacio vacío `arriba`, `abajo`, `izquierda` o
  `derecha`, siempre que el movimiento no saque la ficha fuera del
  tablero. Cada estado tiene entre 2 y 4 acciones válidas según la
  posición del espacio vacío (2 en las esquinas, 3 en los bordes, 4 en el
  centro).

- **Modelo de transición:** aplicar una acción intercambia (`swap`) la
  posición del espacio vacío con la de la ficha vecina correspondiente.

- **Costo de camino:** cada movimiento cuesta 1, por lo que el costo total
  de una solución es simplemente su número de movimientos (costo
  uniforme).

- **Test de objetivo:** `estado == estado_objetivo`.

- **Espacio de estados:** de las 9! = 362 880 permutaciones posibles del
  tablero, solo la mitad (181 440) son alcanzables desde un estado dado,
  porque la paridad de la permutación se conserva bajo los movimientos
  válidos. Esto se usa en `is_solvable()` para verificar que una instancia
  generada aleatoriamente tenga solución, contando el número de
  inversiones de las fichas (ignorando el espacio vacío): es soluble si y
  solo si ese número es par.

### Heurística: distancia Manhattan

```python
def manhattan_distance(state, goal_pos=_GOAL_POS):
    total = 0
    for index, value in enumerate(state):
        if value == 0:
            continue
        r, c = divmod(index, 3)
        gr, gc = goal_pos[value]
        total += abs(r - gr) + abs(c - gc)
    return total
```

Para cada ficha (sin contar el espacio vacío) se suma la distancia
Manhattan entre su fila/columna actual y su fila/columna en el estado
objetivo. Es **admisible** (nunca sobreestima el costo real, porque cada
movimiento desplaza como máximo una ficha una casilla) y **consistente**
(monótona: `h(n) <= costo(n, n') + h(n')` para todo sucesor `n'`), lo que
garantiza que A* con esta heurística sea óptimo y que, al usar la
optimización de "lazy deletion" sobre el mejor costo conocido por estado,
ningún nodo se reabra tras ser cerrado.

---

## 2. Pseudocódigo / código clave comentado

Los tres algoritmos comparten la misma idea de "mejor-primero": extraer de
una frontera el nodo de menor `f(n)` y expandirlo. La diferencia entre A*
y UCS es únicamente la función `f`:

```
UCS:  f(n) = g(n)                       (costo acumulado)
A*:   f(n) = g(n) + h(n)                (costo acumulado + heurística)
BFS:  cola FIFO en vez de cola de prioridad (válido porque el costo
      de cada paso es 1: expandir por niveles == expandir por costo)
```

Núcleo de A* / UCS (`_best_first_search` en `puzzle8.py`), simplificado:

```python
def _best_first_search(start, algorithm_name, heuristic):
    frontier = [(heuristic(start), 0, start_node)]   # min-heap por f(n)
    best_g = {start: 0}                              # mejor g(n) visto por estado
    nodes_expanded = 0

    while frontier:
        _, _, node = heappop(frontier)
        if node.g > best_g.get(node.state, inf):
            continue                                  # entrada obsoleta, se descarta
        if node.state == GOAL:
            return SearchResult(..., encontrado=True)

        nodes_expanded += 1
        for child_state, action in successors(node.state):
            g = node.g + 1
            if g < best_g.get(child_state, inf):
                best_g[child_state] = g
                f = g + heuristic(child_state)         # h=0 para UCS
                heappush(frontier, (f, counter(), child_node))

    return SearchResult(..., encontrado=False)
```

Núcleo de BFS:

```python
def breadth_first_search(start):
    frontier = deque([start_node])
    visited = {start}
    while frontier:
        node = frontier.popleft()
        nodes_expanded += 1
        for child_state, action in successors(node.state):
            if child_state not in visited:
                if child_state == GOAL:
                    return SearchResult(..., encontrado=True)
                visited.add(child_state)
                frontier.append(child_node)
    return SearchResult(..., encontrado=False)
```

Ambas implementaciones cuentan `nodes_expanded` (nodos extraídos de la
frontera y expandidos, sin contar la prueba de objetivo hecha al
generarlos) y `max_frontier_size`, y miden el tiempo con
`time.perf_counter()` alrededor de la búsqueda completa.

---

## 3. Tabla comparativa

Instancias utilizadas (generadas aplicando *N* movimientos aleatorios
válidos desde el estado objetivo, con semilla fija para reproducibilidad):

```
Facil (8 movimientos)          Media (15 movimientos)        Dificil (24 movimientos)       Muy dificil (30 movimientos)
1 5 2                          1 2 3                          8 7 1                           6 8 2
7 4 3                          _ 4 8                          6 4 3                           5 3 7
8 6 _                          5 7 6                          _ 2 5                           _ 1 4
```

| Instancia | Algoritmo | Movimientos (óptimo) | Nodos expandidos | Frontera máx. | Tiempo (s) |
|---|---|---|---|---|---|
| Fácil (8 movimientos) | BFS | 8 | 149 | 112 | 0.001062 |
| Fácil (8 movimientos) | UCS | 8 | 260 | 146 | 0.000995 |
| Fácil (8 movimientos) | A* | 8 | 8 | 8 | 0.000097 |
| Media (15 movimientos) | BFS | 15 | 4 981 | 3 128 | 0.014736 |
| Media (15 movimientos) | UCS | 15 | 8 108 | 4 129 | 0.034748 |
| Media (15 movimientos) | A* | 15 | 197 | 125 | 0.001528 |
| Difícil (24 movimientos) | BFS | 20 | 27 041 | 10 952 | 0.088474 |
| Difícil (24 movimientos) | UCS | 20 | 37 992 | 17 023 | 0.227615 |
| Difícil (24 movimientos) | A* | 20 | 154 | 93 | 0.001070 |
| Muy difícil (30 movimientos) | BFS | 24 | 115 310 | 24 005 | 0.501923 |
| Muy difícil (30 movimientos) | UCS | 24 | 139 315 | 24 053 | 0.978765 |
| Muy difícil (30 movimientos) | A* | 24 | 906 | 515 | 0.009866 |

*(Medido en el entorno de desarrollo usado para esta entrega; los tiempos
absolutos varían según la máquina, pero las proporciones entre algoritmos
son representativas. Nota: el número de movimientos usados para generar
cada instancia es una cota superior de la dificultad, no necesariamente
la distancia óptima real — por eso, por ejemplo, la instancia de "24
movimientos" se resuelve de forma óptima en 20 pasos: el scramble incluyó
movimientos que se deshacían parcialmente entre sí.)*

Promedio de nodos expandidos a través de las 4 instancias:

| Algoritmo | Nodos expandidos (promedio) |
|---|---|
| BFS | 36 870.2 |
| UCS | 46 418.8 |
| A* | 316.2 |

---

## 4. Conclusiones

En las cuatro instancias, los tres algoritmos encontraron exactamente la
misma longitud de solución (óptima), lo cual confirma experimentalmente
que UCS y BFS son óptimos cuando el costo de cada paso es uniforme, y que
A* con la heurística Manhattan también lo es por ser esta admisible. La
diferencia está en el **esfuerzo** necesario para llegar a esa solución:
A* expandió, en promedio, entre 15 y más de 150 veces menos nodos que BFS
y UCS, y esa ventaja crece rápidamente con la dificultad de la instancia
(de una diferencia de ~30x en la instancia fácil a más de 150x en la más
difícil). BFS resultó consistentemente algo más rápido y con menor
consumo de memoria que UCS en este problema, porque con costos de paso
uniformes UCS termina reexplorando el mismo conjunto de estados que BFS
pero con la sobrecarga adicional de mantener una cola de prioridad en
lugar de una simple cola FIFO. En la práctica, para instancias más
difíciles que las probadas aquí (30+ movimientos de mezcla, o el peor
caso del 8-puzzle a 31 movimientos), BFS y UCS se vuelven rápidamente
impracticables en tiempo y memoria, mientras que A* con una buena
heurística sigue siendo viable. Esto ilustra el valor práctico de usar
información del dominio (la heurística) para guiar la búsqueda en lugar
de explorarla a ciegas.

---

## Algorithm Comparison

A* systematically explored the smallest number of nodes across every
instance because its evaluation function f(n) = g(n) + h(n) uses the
Manhattan-distance heuristic to steer expansion toward states that are
actually closer to the goal, whereas BFS and UCS expand nodes purely by
depth or accumulated cost with no notion of "how close" a state is to the
solution. In terms of **time complexity**, both BFS and UCS are
O(b^d) in the worst case, where b is the branching factor (2 to 4 for the
8-puzzle) and d is the depth of the optimal solution, while A* is also
O(b^d) in the worst case but its *effective* branching factor is much
lower in practice whenever the heuristic is informative, which is exactly
what the measured node counts show. **Space complexity** is the main
practical bottleneck for BFS and UCS: both must keep every generated node
in memory (frontier plus explored set), so their memory usage also grows
as O(b^d), and this is visible in the experiment as the "max frontier
size" column, which grows into the tens of thousands of nodes for the
harder instances while A*'s frontier stays two orders of magnitude
smaller. Regarding **completeness**, all three algorithms are complete on
this problem: BFS and UCS are complete whenever b is finite, and A* is
complete as long as the heuristic is finite and the step cost is bounded
below by a positive constant, both of which hold here. Finally, on
**optimality**, BFS is only optimal when step costs are uniform (as they
are in this formulation), UCS is always optimal regardless of step costs
because it always expands the node with the lowest g(n), and A* is
optimal here specifically because the Manhattan-distance heuristic is
admissible and consistent — without that guarantee, A* could return a
suboptimal solution faster instead of the guaranteed-shortest one that
BFS and UCS always find.

---

## Configuración (CONFIG)

```
FULL_NAME = "Andrés Felipe Bolívar Arias"
GITHUB_USER = "<completar con tu usuario de GitHub>"
```
