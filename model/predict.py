import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "modelo.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "features.pkl"))
cooc = joblib.load(os.path.join(BASE_DIR, "cooc_matrix.pkl"))

# =========================
# PREDICCIÓN
# =========================

def predecir_enfermedad(lista_sintomas):
    input_data = pd.DataFrame(0, index=[0], columns=features)

    for sintoma in lista_sintomas:
        if sintoma in input_data.columns:
            input_data.at[0, sintoma] = 1

    probs = model.predict_proba(input_data)[0]
    classes = model.classes_

    resultados = list(zip(classes, probs))
    resultados = sorted(resultados, key=lambda x: x[1], reverse=True)

    return resultados[:3]

# =========================
# SUGERENCIA DE SÍNTOMAS
# =========================

def sugerir_sintomas(lista_sintomas, top_n=5):
    if not lista_sintomas:
        return []

    validos = [s for s in lista_sintomas if s in cooc.columns]

    if not validos:
        return []

    sub = cooc.loc[validos]
    suma = sub.sum().sort_values(ascending=False)

    # eliminar ya seleccionados
    for s in validos:
        if s in suma:
            suma = suma.drop(s)

    return suma.head(top_n).index.tolist()