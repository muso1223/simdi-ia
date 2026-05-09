from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os
import traceback
import streamlit as st


def generar_pdf(datos, diagnostico, examenes):

    try:

        # Ruta base del proyecto
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # Crear carpeta reportes si no existe
        carpeta_reportes = os.path.join(BASE_DIR, "reportes")
        os.makedirs(carpeta_reportes, exist_ok=True)

        # Nombre único del PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_{datos.get('documento', 'sin_doc')}_{timestamp}.pdf"
        ruta_pdf = os.path.join(carpeta_reportes, nombre_archivo)

        # Documento PDF
        doc = SimpleDocTemplate(ruta_pdf)
        styles = getSampleStyleSheet()

        contenido = []

        # Logo
        logo_path = os.path.join(BASE_DIR, "LOGOSIMDI.png")

        if os.path.exists(logo_path):
            logo = Image(logo_path, width=120, height=120)
            contenido.append(logo)

        # Título
        contenido.append(Paragraph("REPORTE CLÍNICO", styles["Title"]))
        contenido.append(Spacer(1, 12))

        # Fechas
        fecha_consulta = datos.get("fecha", "")
        fecha_edicion = datos.get("fecha_edicion", "")

        contenido.append(
            Paragraph(f"Fecha de consulta: {fecha_consulta}", styles["Normal"])
        )

        if fecha_edicion:
            contenido.append(
                Paragraph(f"Fecha de edición: {fecha_edicion}", styles["Normal"])
            )

        contenido.append(Spacer(1, 12))

        # Datos paciente
        contenido.append(Paragraph("Datos del paciente:", styles["Heading2"]))

        contenido.append(
            Paragraph(f"Nombre: {datos.get('nombre', '')}", styles["Normal"])
        )

        contenido.append(
            Paragraph(f"Documento: {datos.get('documento', '')}", styles["Normal"])
        )

        contenido.append(
            Paragraph(f"Edad: {datos.get('edad', '')}", styles["Normal"])
        )

        contenido.append(
            Paragraph(f"Peso: {datos.get('peso', '')} kg", styles["Normal"])
        )

        contenido.append(
            Paragraph(f"Estatura: {datos.get('estatura', '')} m", styles["Normal"])
        )

        contenido.append(
            Paragraph(f"Género: {datos.get('genero', '')}", styles["Normal"])
        )

        contenido.append(Spacer(1, 12))

        # Médico
        contenido.append(Paragraph("Médico responsable:", styles["Heading2"]))

        contenido.append(
            Paragraph(
                f"Nombre: {datos.get('medico_nombre', '')}",
                styles["Normal"]
            )
        )

        contenido.append(
            Paragraph(
                f"Documento: {datos.get('medico_documento', '')}",
                styles["Normal"]
            )
        )

        contenido.append(Spacer(1, 12))

        # Diagnóstico
        contenido.append(Paragraph("Diagnóstico:", styles["Heading2"]))

        if diagnostico:
            for enf, prob in diagnostico:
                contenido.append(
                    Paragraph(f"{enf} ({prob:.2f})", styles["Normal"])
                )
        else:
            contenido.append(
                Paragraph("No hay diagnóstico disponible.", styles["Normal"])
            )

        contenido.append(Spacer(1, 12))

        # Exámenes
        contenido.append(
            Paragraph("Exámenes recomendados:", styles["Heading2"])
        )

        if examenes:
            for enf, lista in examenes.items():

                contenido.append(
                    Paragraph(f"{enf}:", styles["Normal"])
                )

                if lista:
                    for ex in lista:
                        contenido.append(
                            Paragraph(f"- {ex}", styles["Normal"])
                        )
                else:
                    contenido.append(
                        Paragraph("- Sin exámenes registrados", styles["Normal"])
                    )
        else:
            contenido.append(
                Paragraph("No hay exámenes recomendados.", styles["Normal"])
            )

        # Construir PDF
        doc.build(contenido)

        print(f"PDF generado correctamente: {ruta_pdf}")

        return ruta_pdf

    except Exception as e:

        error_completo = traceback.format_exc()

        print("ERROR GENERANDO PDF")
        print(error_completo)

        st.error(f"Error generando PDF: {e}")
        st.code(error_completo)

        return None