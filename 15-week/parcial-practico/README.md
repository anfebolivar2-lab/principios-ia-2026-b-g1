# Parcial practico - Corte 3 (Integracion end-to-end)

Clasificacion con scikit-learn. Dataset por defecto: Breast Cancer Wisconsin (569 muestras, 30 variables).

```bash
pip install -r requirements.txt
python parcial.py                                  # dataset por defecto
python parcial.py --csv datos.csv --target clase   # otro problema
```

## Pasos (segun la rubrica)
1. **Datos**: carga, elimina duplicados/nulos, one-hot para categoricas, split 80/20 estratificado.
2. **Modelo**: Regresion logistica (con escalado) y Random Forest; validacion cruzada de 5 folds; se elige el mejor por F1.
3. **Evaluacion**: Accuracy, F1, matriz de confusion y reporte por clase (resultado: Accuracy y F1 ~ 0.98).
4. **Limitacion etica**: los falsos negativos (maligno clasificado como benigno) retrasan el tratamiento, por lo que accuracy alta no basta; el dataset proviene de una poblacion limitada (sesgo de datos) y el modelo solo debe apoyar, no reemplazar, al medico.

Salidas en `salida/`: `modelo.joblib`, `matriz_confusion.png`.

## Practica
`practica/` trae un ejercicio resuelto (estudiantes aprueba/reprueba, datos sinteticos):
```bash
cd practica && python ../parcial.py --csv estudiantes.csv --target aprobo --etica etica.txt
```
Con `--etica` usas la limitacion de TU problema; sin el, se imprime la de salud.
