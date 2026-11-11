# Resultados

Casos: 569 (train 426, test 143). Maligno = 212, benigno = 357.

| Modelo | CV 5-fold (media +- desv.) | Accuracy test | AUC test |
|---|---|---|---|
| Regresion logistica | 0.979 +- 0.009 | 0.986 | 0.998 |
| Arbol de decision (prof. 3) | 0.939 +- 0.022 | 0.944 | 0.946 |
| kNN (k=5) | 0.967 +- 0.014 | 0.979 | 0.984 |

Mejor AUC en prueba: **Regresion logistica** (0.998).

## Reporte de la regresion logistica
```
precision    recall  f1-score   support

     maligno       0.98      0.98      0.98        53
     benigno       0.99      0.99      0.99        90

    accuracy                           0.99       143
   macro avg       0.99      0.99      0.99       143
weighted avg       0.99      0.99      0.99       143
```
Falsos negativos (tumor maligno clasificado como benigno): **1**.

## Overfitting del arbol
| Profundidad | Train | Test |
|---|---|---|
| 1 | 0.923 | 0.923 |
| 2 | 0.958 | 0.909 |
| 3 | 0.977 | 0.944 |
| 5 | 0.995 | 0.937 |
| 8 | 1.000 | 0.923 |
| 15 | 1.000 | 0.923 |
