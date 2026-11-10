"""Evalua un modelo exportado de Teachable Machine (Keras) sobre imagenes de prueba.
Estructura esperada: prueba/<nombre_clase>/*.jpg  (nombre = clase de labels.txt)."""
import argparse
import os

import numpy as np
from PIL import Image, ImageOps
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from tensorflow.keras.models import load_model

ap = argparse.ArgumentParser()
ap.add_argument("--modelo", default="keras_model.h5")
ap.add_argument("--labels", default="labels.txt")
ap.add_argument("--prueba", default="prueba")
a = ap.parse_args()

model = load_model(a.modelo, compile=False)
# labels.txt: "0 Clase A" -> "Clase A"
clases = [l.strip().split(" ", 1)[1] for l in open(a.labels) if l.strip()]

y_true, y_pred = [], []
for i, c in enumerate(clases):
    carpeta = os.path.join(a.prueba, c)
    for f in os.listdir(carpeta):
        img = Image.open(os.path.join(carpeta, f)).convert("RGB")
        img = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)  # tamano de TM
        x = (np.asarray(img, dtype=np.float32) / 127.5) - 1             # normalizacion de TM
        y_true.append(i)
        y_pred.append(int(np.argmax(model.predict(x[None], verbose=0))))

print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
print(f"F1 (ponderado): {f1_score(y_true, y_pred, average='weighted'):.4f}")
print(confusion_matrix(y_true, y_pred))
print(classification_report(y_true, y_pred, target_names=clases))
