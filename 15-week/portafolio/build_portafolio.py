"""Genera portafolio_competencias_ia.pdf (python build_portafolio.py)."""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

AQUI = os.path.dirname(os.path.abspath(__file__))
AZUL, GRIS, CLARO = colors.HexColor("#1f3a5f"), colors.HexColor("#555555"), colors.HexColor("#eef2f7")
ss = getSampleStyleSheet()
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=10, leading=14.5, spaceAfter=6)
H1 = ParagraphStyle("H1", parent=ss["Heading1"], textColor=AZUL, fontSize=17, spaceBefore=4, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=AZUL, fontSize=12.5, spaceBefore=8, spaceAfter=4)
SM = ParagraphStyle("SM", parent=B, fontSize=8.5, leading=11, textColor=GRIS)
CELL = ParagraphStyle("CELL", parent=B, fontSize=8.8, leading=11.5, spaceAfter=0)
CODE = ParagraphStyle("CODE", fontName="Courier", fontSize=7.8, leading=9.6, backColor=CLARO,
                      borderPadding=5, spaceAfter=8, leftIndent=4)
TITLE = ParagraphStyle("T", parent=H1, fontSize=24, leading=28, spaceAfter=4)


def P(t, s=B): return Paragraph(t, s)
def code(t): return Preformatted(t.strip("\n"), CODE)


def tabla(datos, anchos, cab=True):
    filas = [[Paragraph(str(c), CELL) for c in f] for f in datos]
    t = Table(filas, colWidths=anchos, repeatRows=1 if cab else 0)
    est = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c2d0")),
           ("VALIGN", (0, 0), (-1, -1), "TOP"),
           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CLARO])]
    if cab:
        est += [("BACKGROUND", (0, 0), (-1, 0), AZUL), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
        for i, c in enumerate(datos[0]):
            filas[0][i] = Paragraph(f'<font color="white"><b>{c}</b></font>', CELL)
        t = Table(filas, colWidths=anchos, repeatRows=1)
    t.setStyle(TableStyle(est))
    return t


def pie(c, d):
    c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(GRIS)
    c.drawString(2*cm, 1.2*cm, "Portafolio de Competencias en IA - Andrés Felipe Bolívar Arias - CORHUILA 2026-B")
    c.drawRightString(A4[0]-2*cm, 1.2*cm, f"Pág. {d.page}"); c.restoreState()


s = []
# ---------------- PORTADA ----------------
s += [Spacer(1, 2.5*cm), P("Portafolio de Competencias en IA", TITLE),
      P("Certificación · Corte 3 · Principios de Inteligencia Artificial 2026-B (Grupo V)", H2), Spacer(1, 0.6*cm),
      tabla([["Estudiante", "Andrés Felipe Bolívar Arias"],
             ["Programa", "Ingeniería en Inteligencia Artificial - CORHUILA"],
             ["Repositorio (fork)", "github.com/anfebolivar2-lab/principios-ia-2026-b-g1"],
             ["Entrega", "Individual · Semana 5 del Corte 3 · Valor 5.0"]],
            [4*cm, 12.5*cm], cab=False),
      Spacer(1, 0.8*cm), P("Contenido", H2),
      P("1. Reflexión de aprendizaje &nbsp;&nbsp;2. Los 3 mejores artefactos &nbsp;&nbsp;3. Mapa de competencias "
        "&nbsp;&nbsp;4. Próximos pasos &nbsp;&nbsp;Anexo: cómo reproducir la evidencia."),
      P("Toda la evidencia (código, tablas y capturas) proviene de los archivos del repositorio y de ejecuciones "
        "reales hechas al preparar este documento; las rutas se indican en cada sección.", SM), PageBreak()]

# ---------------- 1. REFLEXION ----------------
s += [P("1. Reflexión de aprendizaje", H1),
      P("<b>El concepto más difícil: que una heurística \"buena\" tiene que ser <i>admisible</i>.</b> Al implementar A* para el "
        "8-puzzle (semana 4) lo difícil no fue escribir la cola de prioridad, sino entender <i>por qué</i> la distancia "
        "Manhattan garantiza una solución óptima: nunca sobreestima, porque cada movimiento desplaza una sola ficha una "
        "casilla. Me costó distinguir \"encuentra una solución\" de \"encuentra la mejor\"; una heurística que sobreestima "
        "haría a A* rápido pero potencialmente incorrecto. Otro detalle que me confundió al inicio: mis instancias "
        "\"de 24 movimientos\" se resolvieron en 20, porque la mezcla aleatoria incluía movimientos que se deshacían entre sí; "
        "el número de movimientos de la mezcla es solo una cota superior de la dificultad real."),
      P("<b>El concepto más revelador: la exactitud no es lo mismo que lo correcto.</b> En el parcial del Corte 3 el modelo "
        "de cáncer de mama alcanzó Accuracy y F1 de 0.98, y mi primera reacción fue dar el trabajo por terminado. Pero la "
        "matriz de confusión muestra <b>1 falso negativo</b>: un tumor maligno clasificado como benigno. En ese contexto un "
        "falso negativo retrasa un tratamiento, así que un solo error no pesa lo mismo que un falso positivo. Lo mismo "
        "aprendí con el ejercicio de práctica (aprobar/reprobar): con accuracy de 0.82 el modelo puede penalizar a quien "
        "trabaja mientras estudia, y una predicción de \"reprobará\" puede volverse una profecía autocumplida. Ahí entendí que "
        "la ética no es un apartado final: cambia qué métrica miro y para qué uso el modelo."),
      P("<b>Cómo cambió mi visión de la IA.</b> Antes la veía como \"un modelo que predice\". Ahora la veo como una cadena: "
        "formular bien el problema (estados, acciones, costo; datos, variable objetivo), elegir un método con sus garantías "
        "(completitud y optimalidad en búsqueda; validación cruzada y métricas por clase en ML), medir con honestidad y "
        "declarar los límites (datos sesgados, poblaciones distintas, decisión final humana). También cambió mi forma de "
        "trabajar: reproducibilidad (semillas fijas, <font face='Courier'>requirements.txt</font>, resultados regenerables "
        "con un script) y documentar las decisiones, no solo entregar código que corre."),
      P("<b>Una autocrítica.</b> En el Corte 1 comparé los algoritmos con una sola medición de tiempo por instancia y solo "
        "cuatro instancias; las proporciones son representativas, pero los tiempos absolutos no son estadísticamente "
        "sólidos. En el Corte 3 mis datos de práctica eran sintéticos, así que sirven para demostrar el flujo, no para "
        "sacar conclusiones sobre estudiantes reales.", B),
      P("<i>Nota: este texto es un borrador redactado a partir de la evidencia del repositorio; ajusta las vivencias "
        "personales (qué se te dificultó y cómo lo resolviste) con tus propias palabras antes de entregar.</i>", SM),
      PageBreak()]

# ---------------- 2. ARTEFACTOS ----------------
s += [P("2. Los 3 mejores artefactos del semestre", H1),
      P("Seleccioné un artefacto por corte, buscando que cada uno muestre un tipo de competencia distinto: "
        "<i>buscar</i> (Corte 1), <i>aprender de datos</i> (Corte 2) y <i>integrar y razonar éticamente</i> (Corte 3).")]

s += [P("Artefacto 1 · Corte 1 - A* vs BFS vs UCS en el 8-puzzle", H2),
      P("<b>Ruta:</b> <font face='Courier'>04-week/03-optional-activity/semana4-busqueda-informada/</font> "
        "(<font face='Courier'>puzzle8.py</font>, <font face='Courier'>compare.py</font>, <font face='Courier'>results.md</font>). "
        "Complemento: agente de laberinto BFS/A* en <font face='Courier'>05-week/03-optional-activity/maze_agent.py</font>."),
      P("<b>Por qué lo elegí:</b> es el trabajo donde mejor se ve el método científico: formulé el espacio de estados completo "
        "(estado, acciones, transición, costo, test de objetivo), verifiqué la solubilidad por paridad de inversiones, implementé tres "
        "algoritmos con la misma interfaz y los comparé con métricas objetivas (nodos expandidos, frontera máxima, tiempo). "
        "El resultado confirma la teoría: los tres hallan la solución óptima, pero A* expande muchísimos menos nodos."),
      code('''
def manhattan_distance(state, goal_pos=_GOAL_POS):
    total = 0
    for index, value in enumerate(state):
        if value == 0:
            continue
        r, c = divmod(index, 3)
        gr, gc = goal_pos[value]
        total += abs(r - gr) + abs(c - gc)
    return total          # admisible y consistente -> A* es optimo
'''),
      tabla([["Instancia", "Algoritmo", "Movs. (óptimo)", "Nodos expandidos", "Frontera máx.", "Tiempo (s)"],
             ["Fácil", "BFS / UCS / A*", "8", "149 / 260 / <b>8</b>", "112 / 146 / 8", "0.0011 / 0.0010 / 0.0001"],
             ["Media", "BFS / UCS / A*", "15", "4 981 / 8 108 / <b>197</b>", "3 128 / 4 129 / 125", "0.0147 / 0.0347 / 0.0015"],
             ["Difícil", "BFS / UCS / A*", "20", "27 041 / 37 992 / <b>154</b>", "10 952 / 17 023 / 93", "0.0885 / 0.2276 / 0.0011"],
             ["Muy difícil", "BFS / UCS / A*", "24", "115 310 / 139 315 / <b>906</b>", "24 005 / 24 053 / 515", "0.5019 / 0.9788 / 0.0099"]],
            [2.2*cm, 2.8*cm, 2.2*cm, 4*cm, 3.2*cm, 3.6*cm]),
      P("Fuente: <font face='Courier'>results.md</font> (salida de <font face='Courier'>compare.py</font>). Promedio de nodos "
        "expandidos: BFS 36 870 · UCS 46 419 · A* 316 (más de 100 veces menos).", SM)]

s += [PageBreak(), P("Artefacto 2 · Corte 2 - Aprendizaje automático", H2),
      tabla([["[COMPLETAR - no hay evidencia del Corte 2 en el repositorio]"],
             ["Las carpetas <font face='Courier'>06-week</font> a <font face='Courier'>10-week</font> están vacías en este fork. "
              "Elige tu mejor trabajo del Corte 2 (regresión lineal/logística, árboles, kNN, Naive Bayes, validación cruzada, "
              "k-means o PCA), súbelo a su carpeta de semana y reemplaza este recuadro con: <b>ruta</b>, <b>por qué lo elegiste</b>, "
              "un <b>fragmento de código</b> y una <b>captura</b> de resultados. Si tu trabajo del Corte 2 no está en Git, agrégalo "
              "(por ejemplo <font face='Courier'>08-week/03-optional-activity/</font>) antes de la entrega."]],
            [16.5*cm]),
      Spacer(1, 4),
      P("Sugerencia de redacción: conecta el artefacto con lo que luego usaste en el parcial (validación cruzada de 5 "
        "folds, matriz de confusión, comparación de modelos), para mostrar la continuidad entre cortes.", SM),
      Spacer(1, 6)]

s += [P("Artefacto 3 · Corte 3 - Clasificación end-to-end con limitación ética", H2),
      P("<b>Ruta:</b> <font face='Courier'>15-week/parcial-practico/</font> (<font face='Courier'>parcial.py</font>, "
        "<font face='Courier'>parcial_colab.ipynb</font>, <font face='Courier'>practica/</font>)."),
      P("<b>Por qué lo elegí:</b> integra todo el flujo: limpieza (duplicados, nulos, one-hot), partición 80/20 estratificada, dos "
        "modelos comparados con validación cruzada de 5 folds, evaluación (Accuracy, F1, matriz de confusión, reporte por clase), "
        "persistencia del modelo y una limitación ética explícita. Además lo hice reutilizable: acepta cualquier CSV "
        "(<font face='Courier'>--csv --target</font>) y una ética propia (<font face='Courier'>--etica</font>), y lo probé con un "
        "segundo problema (estudiantes) para verificar que no estuviera atado al dataset original."),
      code('''
modelos = {
    "Regresion logistica": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
}
for nombre, m in modelos.items():
    m.fit(X_tr, y_tr)
    cv = cross_val_score(m, X_tr, y_tr, cv=5, scoring="f1_weighted").mean()
    ...
mejor = max(resultados, key=lambda k: resultados[k][0])   # se elige por F1
'''),
      code('''
$ python parcial.py            # Breast Cancer Wisconsin: 569 filas, 30 variables
Regresion logistica: CV-F1=0.980 | test Accuracy=0.982 | test F1=0.982
Random Forest:       CV-F1=0.960 | test Accuracy=0.956 | test F1=0.956
=== Mejor modelo: Regresion logistica ===   Accuracy: 0.9825   F1: 0.9825
Matriz de confusion: [[41  1]
                      [ 1 71]]
''')]
img = os.path.join(AQUI, "evidencias", "matriz_confusion.png")
s += [KeepTogether([Image(img, width=6.2*cm, height=6.2*cm*0.8, hAlign="CENTER"),
                    P("Captura: matriz de confusión generada por <font face='Courier'>parcial.py</font> "
                      "(<font face='Courier'>salida/matriz_confusion.png</font>). Un falso negativo (maligno predicho como benigno).", SM)]),
      P("Limitación ética declarada (del propio script): los falsos negativos retrasan un tratamiento y son más graves que un "
        "falso positivo, por lo que accuracy alta no basta; el dataset es pequeño y de una población concreta (sesgo de datos); "
        "y el modelo debe apoyar, no reemplazar, el criterio médico."),
      P("<b>Práctica con datos sintéticos (estudiantes aprueba/reprueba):</b> CV-F1 = 0.811, Accuracy test = 0.817 con "
        "regresión logística. Su limitación ética (profecía autocumplida, sesgo por la variable \"trabaja\") está en "
        "<font face='Courier'>practica/etica.txt</font>.", B),
      PageBreak()]

# ---------------- 3. MAPA ----------------
s += [P("3. Mapa de competencias", H1),
      P("Autoevaluación contra las cuatro competencias del sílabo. Niveles: <b>básico</b> · <b>en desarrollo</b> · <b>logrado</b>. "
        "Procuré calificarme con las mismas exigencias que usaría un evaluador externo.")]
s += [tabla([
    ["Competencia", "Nivel", "Evidencia", "Qué me falta"],
    ["<b>Buscar</b><br/>(algoritmos de búsqueda)", "<b>Logrado</b>",
     "8-puzzle con BFS, UCS y A*: formulación completa, heurística Manhattan admisible, test de solubilidad y comparación "
     "experimental en 4 instancias (<font face='Courier'>04-week/.../results.md</font>). Agente de laberinto BFS/A* "
     "(<font face='Courier'>05-week/.../maze_agent.py</font>).",
     "Probar heurísticas alternativas y búsqueda local/metaheurísticas (hill climbing, genéticos); repetir tiempos varias veces."],
    ["<b>Clasificar</b><br/>(modelos de ML)", "<b>Logrado</b> (flujo) / en desarrollo (profundidad)",
     "Pipeline completo con regresión logística y Random Forest, CV de 5 folds, split estratificado "
     "(<font face='Courier'>15-week/parcial-practico/parcial.py</font>); reutilizado en un segundo problema.",
     "Afinación de hiperparámetros, desbalance de clases, redes neuronales (no tengo evidencia propia de deep learning)."],
    ["<b>Evaluar</b><br/>(métricas y validación)", "<b>En desarrollo</b>",
     "Accuracy, F1 ponderado, matriz de confusión y reporte por clase; comparé modelos por F1 y no solo por accuracy "
     "(captura en Sección 2).",
     "Curvas ROC/PR, intervalos de confianza, evaluación por subgrupos y elegir la métrica según el costo del error "
     "(p. ej. sensibilidad en salud)."],
    ["<b>Razonar éticamente</b>", "<b>En desarrollo</b>",
     "Limitaciones éticas escritas para dos problemas (salud y educación): falsos negativos, sesgo de datos, profecía "
     "autocumplida, decisión final humana (<font face='Courier'>practica/etica.txt</font>).",
     "Pasar del texto a la práctica: medir equidad por grupo, usar datos reales con consentimiento, auditar y documentar "
     "el modelo (model cards)."],
], [3.3*cm, 2.6*cm, 6.4*cm, 4.2*cm]),
    Spacer(1, 6),
    P("<b>Lectura global.</b> Mi punto fuerte es plantear y comparar métodos con rigor en problemas bien definidos. Mi mayor "
      "brecha es llevar la evaluación y la ética de la descripción a la medición (equidad, subgrupos, datos reales). "
      "No califico \"logrado\" en ética porque hoy identifico los riesgos pero todavía no los cuantifico.", B),
    PageBreak()]

# ---------------- 4. PROXIMOS PASOS ----------------
s += [P("4. Próximos pasos", H1),
      P("Priorizo tres áreas que salen directamente de las brechas del mapa de competencias, con acciones concretas y plazos realistas "
        "para compaginar con mis demás materias."),
      tabla([
          ["Área", "Objetivo medible", "Recursos", "Plazo"],
          ["Evaluación de modelos y equidad",
           "Repetir el parcial añadiendo curvas ROC/PR, sensibilidad por clase y métricas por subgrupo; publicar el resultado en el repo.",
           "Curso <i>Machine Learning</i> (Andrew Ng, Coursera/Stanford); documentación de scikit-learn (Model evaluation); "
           "libro <i>Fairness and Machine Learning</i> (Barocas, Hardt, Narayanan, gratuito en línea).",
           "6 semanas"],
          ["Redes neuronales / deep learning",
           "Entrenar una CNN pequeña en un dataset público y compararla con mi baseline de regresión logística.",
           "Curso <i>Deep Learning Specialization</i> (DeepLearning.AI); tutoriales de PyTorch o Keras; "
           "<i>Dive into Deep Learning</i> (d2l.ai).",
           "10 semanas"],
          ["Búsqueda avanzada y razonamiento",
           "Implementar hill climbing / algoritmo genético y minimax con poda alfa-beta y comparar con A*.",
           "<i>Artificial Intelligence: A Modern Approach</i> (Russell y Norvig), caps. 3-6; ejercicios del repositorio de código del libro.",
           "8 semanas"],
          ["IA responsable en la práctica",
           "Escribir una <i>model card</i> para el modelo del parcial y un análisis de riesgos con datos reales.",
           "Guías de IA responsable (p. ej. Google PAIR, Model Cards for Model Reporting); normativa local de protección de datos personales.",
           "4 semanas"],
      ], [3.2*cm, 5.2*cm, 6*cm, 2.1*cm]),
      Spacer(1, 6),
      P("<b>Hábitos que mantendré:</b> seguir versionando cada entrega en Git con un README que explique el problema, el método y "
        "los resultados; fijar semillas y listar dependencias para que cualquiera reproduzca mi trabajo; y construir al menos un "
        "proyecto personal por periodo que combine búsqueda o aprendizaje con un análisis ético explícito.", B),
      Spacer(1, 4),
      P("Anexo · Cómo reproducir la evidencia", H2),
      code('''
# Corte 1
cd 04-week/03-optional-activity/semana4-busqueda-informada && python3 compare.py

# Corte 3
cd 15-week/parcial-practico && pip install -r requirements.txt && python parcial.py
cd practica && python ../parcial.py --csv estudiantes.csv --target aprobo --etica etica.txt

# Regenerar este PDF
pip install reportlab && python 15-week/portafolio/build_portafolio.py
''')]

doc = SimpleDocTemplate(os.path.join(AQUI, "portafolio_competencias_ia.pdf"), pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=2*cm,
                        title="Portafolio de Competencias en IA", author="Andrés Felipe Bolívar Arias")
doc.build(s, onFirstPage=pie, onLaterPages=pie)
print("OK")
