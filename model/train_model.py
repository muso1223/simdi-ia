import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# =========================
# 1. CARGA DE DATOS
# =========================

dataset = pd.read_csv("data/datasett.csv")

print("Datos cargados")
print("Shape:", dataset.shape)

# =========================
# 2. PREPARACIÓN DE DATOS
# =========================

symptom_cols = [col for col in dataset.columns if "Symptom" in col]

symptoms = pd.unique(dataset[symptom_cols].values.ravel())
symptoms = [s for s in symptoms if pd.notnull(s)]

df_binary = pd.DataFrame(0, index=dataset.index, columns=symptoms)

for i in range(len(dataset)):
    for col in symptom_cols:
        val = dataset.iloc[i][col]
        if pd.notnull(val):
            df_binary.at[i, val] = 1

df_binary["Disease"] = dataset["Disease"]

# =========================
# GUARDAR DATASET PROCESADO
# =========================

os.makedirs("../data/processed", exist_ok=True)
df_binary.to_csv("../data/processed/dataset_procesado.csv", index=False)

print("Dataset procesado guardado")

# =========================
# 3. MATRIZ DE CO-OCURRENCIA
# =========================

X_symptoms = df_binary.drop("Disease", axis=1)

cooc_matrix = X_symptoms.T.dot(X_symptoms)

# normalizar
cooc_matrix = cooc_matrix.div(cooc_matrix.max(axis=1), axis=0)

# =========================
# 4. DIVISIÓN DE DATOS
# =========================

X = X_symptoms
y = df_binary["Disease"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Datos divididos")

# =========================
# 5. ENTRENAMIENTO
# =========================

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Modelo entrenado")

# =========================
# 6. EVALUACIÓN
# =========================

y_pred = model.predict(X_test)

print("\n--- RESULTADOS ---")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nReporte:")
print(classification_report(y_test, y_pred))

# =========================
# 7. GUARDAR TODO
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

joblib.dump(model, os.path.join(BASE_DIR, "modelo.pkl"))
joblib.dump(X.columns.tolist(), os.path.join(BASE_DIR, "features.pkl"))
joblib.dump(cooc_matrix, os.path.join(BASE_DIR, "cooc_matrix.pkl"))

print("Modelo, features y matriz de relaciones guardados")