import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ruta = os.path.join(BASE_DIR, "../data/examenes.csv")

df_examenes = pd.read_csv(ruta)

def obtener_examenes(enfermedad):
    resultados = df_examenes[df_examenes["enfermedad"] == enfermedad]

    if resultados.empty:
        return ["Evaluación clínica general"]

    return resultados["examen"].tolist()