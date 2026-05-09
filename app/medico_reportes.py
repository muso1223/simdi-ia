import streamlit as st
import pandas as pd
import os


def medico_reportes(user):

    st.title("Mis Reportes")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ruta_csv = os.path.join(BASE_DIR, "data/reportes/historial.csv")

    if not os.path.exists(ruta_csv):
        st.warning("No existe historial aún")
        return

    df = pd.read_csv(ruta_csv, dtype=str)

    if df.empty:
        st.info("No hay reportes registrados")
        return

    if "medico_documento" not in df.columns:
        st.error("Formato inválido del historial")
        return

    df["medico_documento"] = df["medico_documento"].astype(str).str.strip()
    user_doc = str(user[2]).strip()

    df_medico = df[df["medico_documento"] == user_doc]

    if df_medico.empty:
        st.warning("No tienes reportes asociados")
        return

    st.subheader("Reportes generados")

    # =========================
    # 🔍 BUSCADOR
    # =========================
    busqueda = st.text_input("🔍 Buscar por nombre o documento")

    if busqueda:
        busqueda = busqueda.lower()
        df_medico = df_medico[
            df_medico["nombre"].astype(str).str.lower().str.contains(busqueda) |
            df_medico["documento"].astype(str).str.contains(busqueda)
        ]

    if df_medico.empty:
        st.warning("No se encontraron resultados")
        return

    st.divider()

    # =========================
    # LISTADO
    # =========================
    for idx, row in df_medico.iterrows():

        ruta_pdf = row["ruta_pdf"]

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**{row['nombre']}**")
            st.write(f"Documento: {row['documento']}")
            st.write(f"Fecha: {row['fecha']}")
            st.write(f"Diagnóstico: {row['diagnostico']}")

        with col2:
            if os.path.exists(ruta_pdf):
                with open(ruta_pdf, "rb") as f:
                    st.download_button(
                        "Descargar",
                        f,
                        file_name=os.path.basename(ruta_pdf),
                        key=f"desc_{idx}"
                    )
            else:
                st.error("Archivo no encontrado")

            if st.button("Editar", key=f"edit_{idx}"):

                st.session_state.reporte_editar = {
                    "index": idx,
                    "nombre": row["nombre"],
                    "documento": row["documento"],
                    "edad": row["edad"],
                    "peso": row["peso"],
                    "estatura": row["estatura"],
                    "genero": row["genero"],
                    "fecha": row["fecha"]
                }

                # 🔥 limpiar síntomas SIEMPRE
                st.session_state.sintomas = []

                st.session_state.ir_a_consulta = True
                st.rerun()

        st.divider()