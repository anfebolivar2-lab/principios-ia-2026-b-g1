"""Parcial practico - Corte 3: clasificacion end-to-end con scikit-learn.

Uso:
  python parcial.py                                   # dataset por defecto (cancer de mama)
  python parcial.py --csv datos.csv --target columna  # cualquier CSV con columna objetivo
"""
import argparse
import os

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, classification_report,
                             confusion_matrix, f1_score)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# 1. CARGA Y PREPARACION DE DATOS ------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("--csv")
ap.add_argument("--target", default="target")
ap.add_argument("--etica", help="archivo .txt con la limitacion etica de TU problema")
args = ap.parse_args()

if args.csv:
    df = pd.read_csv(args.csv)
else:
    df = load_breast_cancer(as_frame=True).frame  # target: 0=maligno, 1=benigno

df = df.drop_duplicates().dropna()                 # limpieza basica
X = pd.get_dummies(df.drop(columns=[args.target]))  # categoricas -> numericas
y = df[args.target]
print(f"Datos: {X.shape[0]} filas, {X.shape[1]} variables | clases:\n{y.value_counts()}\n")

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# 2. ENTRENAMIENTO ---------------------------------------------------------
modelos = {
    "Regresion logistica": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
}
resultados = {}
for nombre, m in modelos.items():
    m.fit(X_tr, y_tr)
    cv = cross_val_score(m, X_tr, y_tr, cv=5, scoring="f1_weighted").mean()
    pred = m.predict(X_te)
    resultados[nombre] = (f1_score(y_te, pred, average="weighted"), m, pred)
    print(f"{nombre}: CV-F1={cv:.3f} | test Accuracy={accuracy_score(y_te, pred):.3f} "
          f"| test F1={resultados[nombre][0]:.3f}")

# 3. EVALUACION ------------------------------------------------------------
mejor = max(resultados, key=lambda k: resultados[k][0])
_, modelo_final, pred = resultados[mejor]
print(f"\n=== Mejor modelo: {mejor} ===")
print(f"Accuracy: {accuracy_score(y_te, pred):.4f}")
print(f"F1 (ponderado): {f1_score(y_te, pred, average='weighted'):.4f}")
print("Matriz de confusion:\n", confusion_matrix(y_te, pred))
print(classification_report(y_te, pred))

# Artefactos de la entrega
os.makedirs("salida", exist_ok=True)
joblib.dump(modelo_final, "salida/modelo.joblib")
ConfusionMatrixDisplay.from_predictions(y_te, pred)
plt.title(f"Matriz de confusion - {mejor}")
plt.savefig("salida/matriz_confusion.png", dpi=120, bbox_inches="tight")
print("\nGuardado: salida/modelo.joblib y salida/matriz_confusion.png")

# 4. LIMITACION ETICA ------------------------------------------------------
ETICA_POR_DEFECTO = """LIMITACION ETICA
- Los falsos negativos (tumor maligno clasificado como benigno) retrasan un
  tratamiento y son mas graves que un falso positivo; accuracy alta no basta.
- El dataset (Wisconsin) es pequeno y de una poblacion/equipo clinico concreto:
  puede rendir peor en otros grupos demograficos y hospitales (sesgo de datos).
- Debe ser apoyo al criterio medico, no reemplazarlo (responsabilidad humana)"""
print(open(args.etica, encoding="utf-8").read() if args.etica else ETICA_POR_DEFECTO)
