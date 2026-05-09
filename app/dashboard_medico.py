import streamlit as st
import os
import joblib
import csv
import pandas as pd
from datetime import datetime

from model.predict import predecir_enfermedad, sugerir_sintomas
from model.examenes import obtener_examenes
from app.reportes import generar_pdf
from app.email_service import enviar_correo
from email_validator import validate_email, EmailNotValidError


def medico_panel(user):

    st.title("Sistema de Diagnóstico Médico Inteligente")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    features = joblib.load(os.path.join(BASE_DIR, "model/features.pkl"))

    if "sintomas" not in st.session_state:
        st.session_state.sintomas = []

    # =========================
    # EDICIÓN
    # =========================
    if "reporte_editar" in st.session_state:
        datos_edit = st.session_state.reporte_editar

        st.info("Editando reporte existente")

        nombre_default = datos_edit["nombre"]
        documento_default = str(datos_edit["documento"])
        edad_default = int(datos_edit["edad"])
        peso_default = float(datos_edit["peso"])
        estatura_default = float(datos_edit["estatura"])
        genero_default = datos_edit["genero"]

        # 🔥 SIEMPRE LIMPIO
        st.session_state.sintomas = []

    else:
        nombre_default = ""
        documento_default = ""
        edad_default = 0
        peso_default = 0.0
        estatura_default = 0.0
        genero_default = "Masculino"

    # =========================
    # FORMULARIO
    # =========================
    st.subheader("Datos del paciente")

    col1_form, col2_form = st.columns(2)

    with col1_form:
        nombre = st.text_input("Nombre completo", value=nombre_default)
        documento = st.text_input("Documento", value=documento_default)
        correo = st.text_input("Correo electrónico")
        edad = st.number_input("Edad", min_value=0, max_value=120, value=edad_default)

    with col2_form:
        peso = st.number_input("Peso (kg)", min_value=0.0, value=peso_default)
        estatura = st.number_input("Estatura (m)", min_value=0.0, value=estatura_default)
        genero = st.selectbox(
            "Género",
            ["Masculino", "Femenino", "No aplica"],
            index=["Masculino", "Femenino", "No aplica"].index(genero_default)
        )

    # =========================
    # SÍNTOMAS
    # =========================
    col1, col2 = st.columns([2, 1])

    with col1:
        seleccion = st.multiselect(
            "Seleccione los síntomas",
            options=features,
            default=st.session_state.sintomas
        )
        st.session_state.sintomas = seleccion

    with col2:
        st.subheader("Sugerencias")

        if st.session_state.sintomas:
            sugeridos = sugerir_sintomas(st.session_state.sintomas)

            for s in sugeridos:
                if st.button(s, key=f"sug_{s}"):
                    if s not in st.session_state.sintomas:
                        st.session_state.sintomas.append(s)
                        st.rerun()

    st.divider()

    # =========================
    # GENERAR / EDITAR
    # =========================
    if st.button("Generar reporte completo"):

        # =========================
        # VALIDACIONES
        # =========================

        if not nombre.strip():
            st.warning("El nombre es obligatorio")
            return

        if len(nombre.strip()) < 3:
            st.warning("Nombre inválido")
            return

        if not documento.strip():
            st.warning("El documento es obligatorio")
            return

        if not documento.isdigit():
            st.warning("El documento debe ser numérico")
            return

        if edad <= 0 or edad > 120:
            st.warning("Edad inválida")
            return

        if peso <= 0 or peso > 400:
            st.warning("Peso inválido")
            return

        if estatura <= 0 or estatura > 3:
            st.warning("Estatura inválida")
            return

        if correo:

            try:
                validate_email(correo)

            except EmailNotValidError:
                st.warning("Correo inválido")
                return

        elif not st.session_state.sintomas:
            st.warning("Seleccione síntomas")

        else:

            with st.spinner("Procesando..."):

                try:

                    diagnostico = predecir_enfermedad(st.session_state.sintomas)

                    examenes_dict = {
                        enf: obtener_examenes(enf)
                        for enf, _ in diagnostico
                    }

                    ruta_csv = os.path.join(BASE_DIR, "data/reportes/historial.csv")
                    os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)

                    mensaje_final = ""

                    # =========================
                    # EDICIÓN
                    # =========================
                    if "reporte_editar" in st.session_state and os.path.exists(ruta_csv):

                        df = pd.read_csv(ruta_csv, dtype=str)
                        idx = st.session_state.reporte_editar["index"]

                        fecha_original = df.loc[idx, "fecha"]
                        fecha_edicion = datetime.now().strftime("%Y-%m-%d %H:%M")

                        datos = {
                            "nombre": nombre,
                            "documento": str(documento),
                            "edad": edad,
                            "peso": peso,
                            "estatura": estatura,
                            "genero": genero,
                            "medico_nombre": user[1],
                            "medico_documento": str(user[2]),
                            "fecha": fecha_original,
                            "fecha_edicion": fecha_edicion
                        }

                        ruta_pdf = os.path.abspath(
                            generar_pdf(datos, diagnostico, examenes_dict)
                        )

                        ruta_vieja = df.loc[idx, "ruta_pdf"]

                        if os.path.exists(ruta_vieja):
                            os.remove(ruta_vieja)

                        df.loc[idx, "nombre"] = nombre
                        df.loc[idx, "documento"] = str(documento)
                        df.loc[idx, "edad"] = str(edad)
                        df.loc[idx, "peso"] = str(peso)
                        df.loc[idx, "estatura"] = str(estatura)
                        df.loc[idx, "genero"] = genero
                        df.loc[idx, "diagnostico"] = "; ".join(
                            [f"{e} ({p:.2f})" for e, p in diagnostico]
                        )
                        df.loc[idx, "ruta_pdf"] = ruta_pdf
                        df.loc[idx, "fecha_edicion"] = fecha_edicion

                        df.to_csv(ruta_csv, index=False)

                        del st.session_state.reporte_editar

                        mensaje_final = "Reporte editado correctamente"

                    # =========================
                    # NUEVO
                    # =========================
                    else:

                        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

                        datos = {
                            "nombre": nombre,
                            "documento": str(documento),
                            "edad": edad,
                            "peso": peso,
                            "estatura": estatura,
                            "genero": genero,
                            "medico_nombre": user[1],
                            "medico_documento": str(user[2]),
                            "fecha": fecha,
                            "fecha_edicion": ""
                        }

                        ruta_pdf = os.path.abspath(
                            generar_pdf(datos, diagnostico, examenes_dict)
                        )

                        file_exists = os.path.isfile(ruta_csv)

                        with open(ruta_csv, "a", newline="", encoding="utf-8") as f:

                            writer = csv.writer(f)

                            if not file_exists:
                                writer.writerow([
                                    "nombre", "documento", "edad", "peso",
                                    "estatura", "genero",
                                    "medico_nombre", "medico_documento",
                                    "fecha", "fecha_edicion",
                                    "diagnostico", "ruta_pdf"
                                ])

                            writer.writerow([
                                nombre, str(documento), edad, peso,
                                estatura, genero,
                                user[1], str(user[2]),
                                fecha, "",
                                "; ".join([f"{e} ({p:.2f})" for e, p in diagnostico]),
                                ruta_pdf
                            ])

                        mensaje_final = "Reporte generado y guardado"

                    # =========================
                    # CORREO
                    # =========================
                    if correo:

                        try:
                            enviar_correo(correo, ruta_pdf)
                            mensaje_final += " y enviado al correo"

                        except Exception:
                            mensaje_final += " (error al enviar correo)"

                    st.success(mensaje_final + " ✅")

                    # =========================
                    # DESCARGA
                    # =========================
                    if os.path.exists(ruta_pdf):

                        with open(ruta_pdf, "rb") as f:

                            st.download_button(
                                "Descargar reporte",
                                f,
                                file_name=os.path.basename(ruta_pdf)
                            )

                    else:
                        st.error("No se encontró el PDF")

                except Exception as e:

                    import traceback

                    st.error(f"ERROR: {e}")
                    st.code(traceback.format_exc())

    # =========================
    # BOTÓN PERMANENTE PARA VER REPORTES
    # =========================
    st.divider()
    if st.button("Ver reportes"):
        st.session_state.view = "reportes_medico"
        st.rerun()