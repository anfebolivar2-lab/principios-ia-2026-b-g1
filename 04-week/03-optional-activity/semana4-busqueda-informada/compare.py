"""
compare.py
==========

Ejecuta A*, BFS y UCS sobre varias instancias del 8-puzzle y compara:
    - Longitud del camino encontrado (numero de movimientos)
    - Nodos expandidos
    - Tamano maximo de la frontera (proxy del uso de memoria)
    - Tiempo de ejecucion (segundos)

Genera una tabla en formato Markdown (tambien la imprime en consola) que
se usa directamente en el README.md del informe.
"""

from __future__ import annotations

import statistics
from typing import List

from puzzle8 import (
    GOAL,
    SearchResult,
    astar,
    breadth_first_search,
    is_solvable,
    render,
    scramble,
    uniform_cost_search,
)

# Tres instancias de dificultad creciente (numero de movimientos aleatorios
# aplicados desde el estado objetivo). Se usa una semilla fija por instancia
# para que los resultados sean reproducibles.
INSTANCES = [
    ("Facil (8 movimientos)", scramble(8, seed=1)),
    ("Media (15 movimientos)", scramble(15, seed=2)),
    ("Dificil (24 movimientos)", scramble(24, seed=3)),
    ("Muy dificil (30 movimientos)", scramble(30, seed=4)),
]

ALGORITHMS = [
    ("BFS", breadth_first_search),
    ("UCS", uniform_cost_search),
    ("A*", astar),
]


def run_all() -> List[dict]:
    rows = []
    for label, state in INSTANCES:
        assert is_solvable(state), f"Instancia no resoluble: {state}"
        for algo_name, algo_fn in ALGORITHMS:
            result: SearchResult = algo_fn(state)
            rows.append(
                {
                    "instancia": label,
                    "algoritmo": algo_name,
                    "encontrado": result.found,
                    "longitud_camino": result.path_length,
                    "nodos_expandidos": result.nodes_expanded,
                    "frontera_max": result.max_frontier_size,
                    "tiempo_s": result.time_seconds,
                }
            )
    return rows


def to_markdown_table(rows: List[dict]) -> str:
    header = (
        "| Instancia | Algoritmo | Movimientos (optimo) | Nodos expandidos | "
        "Frontera max. | Tiempo (s) |\n"
        "|---|---|---|---|---|---|\n"
    )
    lines = []
    for r in rows:
        lines.append(
            f"| {r['instancia']} | {r['algoritmo']} | {r['longitud_camino']} | "
            f"{r['nodos_expandidos']} | {r['frontera_max']} | {r['tiempo_s']:.6f} |"
        )
    return header + "\n".join(lines)


def print_instances():
    print("Instancias utilizadas:\n")
    for label, state in INSTANCES:
        print(f"-- {label} --")
        print(render(state))
        print()


if __name__ == "__main__":
    print_instances()
    rows = run_all()
    table = to_markdown_table(rows)
    print(table)

    with open("results.md", "w", encoding="utf-8") as f:
        f.write(table + "\n")

    # Resumen rapido: promedio de nodos expandidos por algoritmo (a traves
    # de las 3 instancias), util para las conclusiones del informe.
    print("\nPromedio de nodos expandidos por algoritmo:")
    for algo_name, _ in ALGORITHMS:
        vals = [r["nodos_expandidos"] for r in rows if r["algoritmo"] == algo_name]
        print(f"  {algo_name}: {statistics.mean(vals):.1f}")
