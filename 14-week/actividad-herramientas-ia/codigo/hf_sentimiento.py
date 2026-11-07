import time
from transformers import pipeline
t=time.time()
clf=pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
print("cargado en",round(time.time()-t,1),"s")
frases=["Me encantó la clase de hoy, aprendí muchísimo.","El servicio fue pésimo y nadie me ayudó.","Mañana hay parcial a las 8.","Qué belleza, otra vez se fue la luz.","Ese parcero es una chimba.","No estuvo nada mal."]
for f in frases:
    r=clf(f)[0]; print(f"{f}|{r['label']}|{r['score']:.3f}")
