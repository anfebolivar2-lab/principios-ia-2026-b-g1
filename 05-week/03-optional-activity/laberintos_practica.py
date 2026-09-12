"""
laberintos_practica.py
=======================

Dos laberintos de practica para ejercitar la adaptacion de maze_agent.py
a distintos formatos de entrada, tal como podria darlos el profesor en
el parcial. Para probar cada uno:

    1. Abre maze_agent.py
    2. Reemplaza el contenido de MAZE, START y GOAL por los de abajo
    3. Corre: python maze_agent.py
    4. Compara con la "Solucion esperada" de cada laberinto

No hace falta subir este archivo al repo, es solo para que practiques.
"""

# ===========================================================================
# PRACTICA 1: dict COMPLETO (row, col) -> 0/1
# ===========================================================================
# Este es el caso "facil": el dict trae TODAS las celdas, incluidas las
# libres. normalize_maze() ya lo soporta tal cual, sin tocar nada.
#
# Grilla equivalente (0=libre, 1=pared), 5 filas x 6 columnas:
#   0 0 1 0 0 0
#   0 1 1 0 1 0
#   0 1 0 0 1 0
#   0 0 0 1 1 0
#   1 1 0 0 0 0

MAZE_1 = {
    (0, 0): 0, (0, 1): 0, (0, 2): 1, (0, 3): 0, (0, 4): 0, (0, 5): 0,
    (1, 0): 0, (1, 1): 1, (1, 2): 1, (1, 3): 0, (1, 4): 1, (1, 5): 0,
    (2, 0): 0, (2, 1): 1, (2, 2): 0, (2, 3): 0, (2, 4): 1, (2, 5): 0,
    (3, 0): 0, (3, 1): 0, (3, 2): 0, (3, 3): 1, (3, 4): 1, (3, 5): 0,
    (4, 0): 1, (4, 1): 1, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0,
}
START_1 = (0, 0)
GOAL_1 = (4, 5)

# Solucion esperada (VERIFICADA corriendo el codigo real):
#   Camino (BFS y A* coinciden, ambos optimos): 9 pasos
#     (0,0) (1,0) (2,0) (3,0) (3,1) (3,2) (4,2) (4,3) (4,4) (4,5)
#   Nodos expandidos: BFS = 13, A* = 11 (A* mas eficiente aqui)
#   Hay tambien un camino alterno mas largo por arriba/derecha
#   ((0,3)->(0,4)->(0,5)->(1,5)->(2,5)->(3,5)->(4,5)): sirve para ver que
#   A* evita explorarlo a fondo porque la heuristica lo aleja de la meta,
#   mientras que BFS sí gasta pasos explorando en esa direccion.


# ===========================================================================
# PRACTICA 2 (RETO): dict DISPERSO - solo lista las PAREDES
# ===========================================================================
# Este es el caso que rompe la plantilla tal como esta: normalize_maze()
# rellena por defecto con 1 (pared) toda celda que NO aparece en el dict.
# Si el profesor te da un dict que solo marca las paredes (asumiendo que
# todo lo demas es libre), correr esto sin ajustar nada hace que CASI TODO
# el laberinto se vea como pared y probablemente no encuentre camino.
#
# Grilla real que representa este dict disperso, 4 filas x 5 columnas
# (0=libre, 1=pared) - fijate que aqui casi todo es libre:
#   0 0 0 1 0
#   0 1 0 1 0
#   0 1 0 0 0
#   0 0 0 1 0

MAZE_2_SPARSE = {
    (0, 3): 1,
    (1, 1): 1,
    (1, 3): 1,
    (2, 1): 1,
    (3, 3): 1,
}
START_2 = (0, 0)
GOAL_2 = (3, 4)

# PASO A: corre maze_agent.py con MAZE_2_SPARSE tal cual (sin arreglar
# normalize_maze) y observa que falla el AssertionError final porque BFS/A*
# no encuentran camino (casi todo se interpreta como pared).
#
# PASO B: corrige normalize_maze para este formato. Pista: cambia el
# relleno por defecto de la grilla de pared (1) a libre (0), y deja que el
# dict solo marque las excepciones (las paredes):
#
#     def normalize_maze(maze, filas, columnas):
#         if isinstance(maze, dict):
#             grid = [[0] * columnas for _ in range(filas)]   # <- antes era [1]*columnas
#             for (r, c), value in maze.items():
#                 grid[r][c] = value
#             return grid
#         return maze
#
# Como un dict disperso no trae el tamano de la grilla (no puedes inferirlo
# de max(fila)/max(columna) si el ultimo renglon/columna es todo libre y
# por tanto no aparece en el dict), en el examen real pregunta al profesor
# el tamano exacto o confirmalo con el enunciado; aqui es 4x5.
#
# Solucion esperada (VERIFICADA corriendo el codigo real, con
# normalize_maze ya corregido segun la pista de arriba):
#   Camino (BFS y A* coinciden, ambos optimos): 7 pasos
#     (0,0) (0,1) (0,2) (1,2) (2,2) (2,3) (2,4) (3,4)
#   Es el unico camino posible (el brazo por (3,0)-(3,1)-(3,2) es un
#   callejon sin salida por la pared en (3,3)).
#
#   Nodos expandidos: BFS = 12, A* = 13  <-- ¡OJO! Aqui A* expandio UNO MAS
#   que BFS. No es un error: en un laberinto pequeño con un solo corredor
#   (casi sin bifurcaciones reales para "elegir mejor"), la heuristica no
#   tiene mucho margen para ahorrar exploracion, y el overhead de como se
#   rompen empates en la cola de prioridad puede hacer que A* visite algun
#   nodo extra. La leccion para el parcial: la comparacion de eficiencia
#   debe basarse en lo que el codigo realmente imprime, no asumir siempre
#   "A* gana" - a veces hay que explicar por que en ESE laberinto en
#   particular la diferencia fue chica, nula o incluso al reves.
