import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================
# 1. CARGA DE DATOS
# =========================

dataset = pd.read_csv("data/datasett.csv")
description = pd.read_csv("data/symptom_Description.csv")
precaution = pd.read_csv("data/symptom_precaution.csv")
severity = pd.read_csv("data/Symptom-severity.csv")

colombia = pd.read_csv("data/88._Analisis_de_Registros_Individuales_de_prestación_de_Servicios_de_Salud-RIPS_en_Bucaramanga_-_Consulta_Externa_20260318.csv")

print("Datos cargados correctamente")

# Verificación
print("Archivo usado:", os.path.abspath("data/datasett.csv"))
print("Shape inicial:", dataset.shape)

# =========================
# 2. EXPLORACIÓN (SIN MODIFICAR DATOS)
# =========================

symptom_cols = [col for col in dataset.columns if "Symptom" in col]

# =========================
# 3. FEATURE ENGINEERING (NO ALTERA DATOS)
# =========================

dataset["num_sintomas"] = dataset[symptom_cols].apply(lambda x: sum(pd.notnull(x)), axis=1)

# =========================
# 4. MATRIZ BINARIA (SOLO PARA ANÁLISIS)
# =========================

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
# 5. ANÁLISIS EXPLORATORIO
# =========================

# 5.1 Enfermedades
plt.figure()
dataset["Disease"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Enfermedades")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------

# 5.2 Número de síntomas
plt.figure()
plt.hist(dataset["num_sintomas"])
plt.title("Distribución del número de síntomas")
plt.xlabel("Cantidad")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.show()

# -------------------------

# 5.3 Síntomas más frecuentes
sintomas = dataset[symptom_cols].values.flatten()
sintomas = pd.Series(sintomas)
sintomas = sintomas.dropna()

plt.figure()
sintomas.value_counts().head(10).plot(kind="bar")
plt.title("Top 10 síntomas más frecuentes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------

# 5.4 Severidad
if "weight" in severity.columns:
    plt.figure()
    plt.hist(severity["weight"])
    plt.title("Distribución de severidad de síntomas")
    plt.xlabel("Peso")
    plt.tight_layout()
    plt.show()

# -------------------------

# 5.5 Colombia
print("\nColumnas dataset Colombia:")
print(colombia.columns)

if "Diagnostico_principal" in colombia.columns:
    plt.figure()
    colombia["Diagnostico_principal"].value_counts().head(10).plot(kind="bar")
    plt.title("Top 10 diagnósticos en Colombia")
    plt.xticks(rotation=60)
    plt.tight_layout()
    plt.show()

# =========================
# 6. BOXPLOTS
# =========================

plt.figure()
plt.boxplot(dataset["num_sintomas"])
plt.title("Boxplot - Número de síntomas")
plt.ylabel("Cantidad")
plt.show()

if "Edad" in colombia.columns:
    colombia["Edad"] = pd.to_numeric(colombia["Edad"], errors="coerce")

    plt.figure()
    plt.boxplot(colombia["Edad"].dropna())
    plt.title("Boxplot - Edad pacientes")
    plt.ylabel("Edad")
    plt.show()

if "weight" in severity.columns:
    plt.figure()
    plt.boxplot(severity["weight"].dropna())
    plt.title("Boxplot - Severidad síntomas")
    plt.ylabel("Peso")
    plt.show()

# =========================
# 7. OUTLIERS (IQR)
# =========================

q1 = dataset["num_sintomas"].quantile(0.25)
q3 = dataset["num_sintomas"].quantile(0.75)
iqr = q3 - q1

outliers = dataset[
    (dataset["num_sintomas"] < q1 - 1.5 * iqr) |
    (dataset["num_sintomas"] > q3 + 1.5 * iqr)
]

print("Cantidad de outliers:", len(outliers))

# =========================
# 8. MATRIZ DE CORRELACIÓN (TOP 10)
# =========================

top_symptoms = df_binary.drop("Disease", axis=1).sum().sort_values(ascending=False).head(10).index

df_top = df_binary[top_symptoms]
corr = df_top.corr()

plt.figure(figsize=(8, 6))

sns.heatmap(
    corr,
    cmap="coolwarm",
    annot=True,
    linewidths=0.5,
    square=True
)

plt.title("Correlación entre los 10 síntomas más frecuentes")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# =========================
# 9. HISTOGRAMA EDAD
# =========================

if "Edad" in colombia.columns:
    plt.figure()
    plt.hist(colombia["Edad"].dropna())
    plt.title("Distribución de edad")
    plt.xlabel("Edad")
    plt.ylabel("Frecuencia")
    plt.show()

# =========================
# 10. RESUMEN FINAL
# =========================

print("\n--- RESUMEN ---")
print(f"Total enfermedades: {dataset['Disease'].nunique()}")
print(f"Total síntomas únicos: {len(symptoms)}")
print(f"Promedio síntomas: {dataset['num_sintomas'].mean():.2f}")
print("Media:", dataset["num_sintomas"].mean())
print("Mediana:", dataset["num_sintomas"].median())
print("Moda:", dataset["num_sintomas"].mode()[0])

# =========================
# 11. INFORMACIÓN GENERAL
# =========================

print("\n========== INFORMACIÓN GENERAL ==========")

# Dataset principal
print("\n--- DATASET PRINCIPAL ---")
print(f"Filas: {dataset.shape[0]}")
print(f"Columnas: {dataset.shape[1]}")

print("\nValores nulos:")
print(dataset.isnull().sum())

print("\nTotal nulos:")
print(dataset.isnull().sum().sum())

# DUPLICADOS
duplicados = dataset.duplicated().sum()
print(f"\nRegistros duplicados: {duplicados}")

# -------------------------

print("\n--- DATASET COLOMBIA ---")
print(f"Filas: {colombia.shape[0]}")
print(f"Columnas: {colombia.shape[1]}")

print("\nValores nulos:")
print(colombia.isnull().sum())

print("\nTotal nulos:")
print(colombia.isnull().sum().sum())