"""Genera estudiantes.csv (datos sinteticos) para practicar el parcial."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
n = 300
df = pd.DataFrame({
    "horas_estudio": rng.uniform(0, 20, n).round(1),
    "asistencia": rng.uniform(40, 100, n).round(0),
    "nota_previa": rng.uniform(1, 5, n).round(1),
    "trabaja": rng.integers(0, 2, n),
})
score = (0.15 * df.horas_estudio + 0.03 * df.asistencia + 0.6 * df.nota_previa
         - 0.5 * df.trabaja + rng.normal(0, 0.8, n))
df["aprobo"] = (score > score.median()).astype(int)
df.to_csv("estudiantes.csv", index=False)
print(df.head())
