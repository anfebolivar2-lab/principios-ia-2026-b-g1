# Version Teachable Machine (imagenes / audio / poses)

Teachable Machine entrena en el navegador (https://teachablemachine.withgoogle.com), asi que el "codigo" es el proceso + la evaluacion.

## Pasos (80 min)
1. **Datos**: nuevo proyecto > *Image Project* > *Standard*. Crea una clase por categoria y captura 50-100 imagenes por clase con la webcam (varia fondo, luz y angulo).
   Reserva ~20% de las capturas como **prueba**: tomalas aparte, NO las uses para entrenar.
2. **Entrenar**: *Training* con 50 epochs, batch 16, learning rate 0.001 (valores por defecto).
3. **Evaluar**: en la pestana *Advanced > Under the hood* anota Accuracy por clase y la matriz de confusion que muestra. Para una metrica propia, usa `evaluar_tm.py`.
4. **Exportar**: *Export Model > Tensorflow > Keras* y descarga `keras_model.h5` y `labels.txt`. Guarda las imagenes de prueba en `prueba/<clase>/*.jpg`.
5. **Subir a GitHub**: modelo, `labels.txt`, carpeta `prueba/` y capturas de pantalla de las metricas.

```bash
pip install tensorflow pillow scikit-learn
python evaluar_tm.py --modelo keras_model.h5 --labels labels.txt --prueba prueba/
```
