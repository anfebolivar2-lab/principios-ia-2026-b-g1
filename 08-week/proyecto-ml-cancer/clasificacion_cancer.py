"""
Mini-proyecto de Machine Learning (Corte 2): clasificar tumores benignos/malignos.

Dataset: Breast Cancer Wisconsin (incluido en scikit-learn, 569 casos, 30 variables).
Cubre: regresion logistica, arbol de decision y kNN, validacion cruzada,
matriz de confusion, curva ROC y demostracion de overfitting (profundidad del arbol).

Ejecutar:  python3 clasificacion_cancer.py   (genera figuras/ y resultados.md)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (confusion_matrix, ConfusionMatrixDisplay, classification_report,
                             roc_curve, roc_auc_score)

SEED = 42
data = load_breast_cancer()
X, y = data.data, data.target            # y: 0 = maligno, 1 = benigno
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=SEED)

modelos = {
    "Regresion logistica": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "Arbol de decision (prof. 3)": DecisionTreeClassifier(max_depth=3, random_state=SEED),
    "kNN (k=5)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
out = ["# Resultados\n", f"Casos: {len(y)} (train {len(y_tr)}, test {len(y_te)}). Maligno = {int((y==0).sum())}, benigno = {int((y==1).sum())}.\n",
       "| Modelo | CV 5-fold (media +- desv.) | Accuracy test | AUC test |", "|---|---|---|---|"]
fig, ax = plt.subplots(1, 3, figsize=(13, 4))
rocfig, rax = plt.subplots(figsize=(5, 4.5))
mejor, mejor_auc = None, 0
for i, (nombre, m) in enumerate(modelos.items()):
    cvs = cross_val_score(m, X_tr, y_tr, cv=cv)
    m.fit(X_tr, y_tr)
    pred = m.predict(X_te); proba = m.predict_proba(X_te)[:, 1]
    acc = (pred == y_te).mean(); auc = roc_auc_score(y_te, proba)
    out.append(f"| {nombre} | {cvs.mean():.3f} +- {cvs.std():.3f} | {acc:.3f} | {auc:.3f} |")
    ConfusionMatrixDisplay(confusion_matrix(y_te, pred), display_labels=["maligno", "benigno"]).plot(ax=ax[i], colorbar=False)
    ax[i].set_title(f"{nombre}\nacc={acc:.3f}")
    fpr, tpr, _ = roc_curve(y_te, proba); rax.plot(fpr, tpr, label=f"{nombre} (AUC {auc:.3f})")
    if auc > mejor_auc: mejor, mejor_auc = nombre, auc
    if nombre.startswith("Regresion"):
        rep = classification_report(y_te, pred, target_names=["maligno", "benigno"])
        fn = int(((pred == 1) & (y_te == 0)).sum())
fig.tight_layout(); fig.savefig("figuras/matrices_confusion.png", dpi=130)
rax.plot([0, 1], [0, 1], "k--", lw=1); rax.set_xlabel("Tasa de falsos positivos"); rax.set_ylabel("Tasa de verdaderos positivos")
rax.set_title("Curvas ROC (conjunto de prueba)"); rax.legend(fontsize=7, loc="lower right"); rocfig.tight_layout(); rocfig.savefig("figuras/roc.png", dpi=130)

# --- Overfitting: profundidad del arbol vs. accuracy train/test
prof = range(1, 16); tr, te = [], []
for d in prof:
    t = DecisionTreeClassifier(max_depth=d, random_state=SEED).fit(X_tr, y_tr)
    tr.append(t.score(X_tr, y_tr)); te.append(t.score(X_te, y_te))
plt.figure(figsize=(6, 4)); plt.plot(prof, tr, "o-", label="entrenamiento"); plt.plot(prof, te, "s-", label="prueba")
plt.xlabel("Profundidad maxima del arbol"); plt.ylabel("Accuracy"); plt.title("Overfitting: el arbol memoriza el entrenamiento"); plt.legend(); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig("figuras/overfitting.png", dpi=130)

out += ["", f"Mejor AUC en prueba: **{mejor}** ({mejor_auc:.3f}).", "",
        "## Reporte de la regresion logistica", "```", rep.strip(), "```",
        f"Falsos negativos (tumor maligno clasificado como benigno): **{fn}**.", "",
        "## Overfitting del arbol", "| Profundidad | Train | Test |", "|---|---|---|"]
out += [f"| {d} | {a:.3f} | {b:.3f} |" for d, a, b in zip(prof, tr, te) if d in (1, 2, 3, 5, 8, 15)]
open("resultados.md", "w").write("\n".join(out) + "\n")
print("\n".join(out))
