import pandas as pd
import streamlit as st
import os


def admin_reportes():

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ruta_csv = os.path.join(BASE_DIR, "data/reportes/historial.csv")

    # =========================
    # VALIDACIÓN
    # =========================
    if not os.path.exists(ruta_csv):
        st.warning("No hay reportes registrados")
        return

    df = pd.read_csv(ruta_csv)

    if df.empty:
        st.info("No hay reportes disponibles")
        return

    st.subheader("Reportes generados")

    # =========================
    # 🔍 BUSCADOR
    # =========================
    busqueda = st.text_input("🔍 Buscar por nombre o documento")

    if busqueda:
        busqueda = busqueda.lower()
        df = df[
            df["nombre"].astype(str).str.lower().str.contains(busqueda) |
            df["documento"].astype(str).str.contains(busqueda)
        ]

    if df.empty:
        st.warning("No se encontraron resultados")
        return

    st.divider()

    # =========================
    # LISTADO
    # =========================
    for i, row in df.iterrows():

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
                        key=f"desc_{i}"
                    )
            else:
                st.error("Archivo no encontrado")

        st.divider()