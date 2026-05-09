from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os


def generar_pdf(datos, diagnostico, examenes):

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    carpeta_reportes = os.path.join(BASE_DIR, "reportes")
    os.makedirs(carpeta_reportes, exist_ok=True)

    # Nombre único
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"reporte_{datos['documento']}_{timestamp}.pdf"
    ruta_pdf = os.path.join(carpeta_reportes, nombre_archivo)

    doc = SimpleDocTemplate(ruta_pdf)
    styles = getSampleStyleSheet()

    contenido = []

    logo_path = os.path.join(BASE_DIR, "LOGOSIMDI.png")

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=120, height=120)
        contenido.append(logo)

    contenido.append(Paragraph("REPORTE CLÍNICO", styles["Title"]))
    contenido.append(Spacer(1, 12))

    # Fechas
    fecha_consulta = datos.get("fecha", "")
    fecha_edicion = datos.get("fecha_edicion", "")

    contenido.append(Paragraph(f"Fecha de consulta: {fecha_consulta}", styles["Normal"]))

    if fecha_edicion:
        contenido.append(Paragraph(f"Fecha de edición: {fecha_edicion}", styles["Normal"]))

    contenido.append(Spacer(1, 12))

    # Paciente
    contenido.append(Paragraph("Datos del paciente:", styles["Heading2"]))
    contenido.append(Paragraph(f"Nombre: {datos['nombre']}", styles["Normal"]))
    contenido.append(Paragraph(f"Documento: {datos['documento']}", styles["Normal"]))
    contenido.append(Paragraph(f"Edad: {datos['edad']}", styles["Normal"]))
    contenido.append(Paragraph(f"Peso: {datos['peso']} kg", styles["Normal"]))
    contenido.append(Paragraph(f"Estatura: {datos['estatura']} m", styles["Normal"]))
    contenido.append(Paragraph(f"Género: {datos['genero']}", styles["Normal"]))

    contenido.append(Spacer(1, 12))

    # Médico
    contenido.append(Paragraph("Médico responsable:", styles["Heading2"]))
    contenido.append(Paragraph(f"Nombre: {datos.get('medico_nombre', '')}", styles["Normal"]))
    contenido.append(Paragraph(f"Documento: {datos.get('medico_documento', '')}", styles["Normal"]))

    contenido.append(Spacer(1, 12))

    # Diagnóstico
    contenido.append(Paragraph("Diagnóstico:", styles["Heading2"]))
    for enf, prob in diagnostico:
        contenido.append(Paragraph(f"{enf} ({prob:.2f})", styles["Normal"]))

    contenido.append(Spacer(1, 12))

    # Exámenes
    contenido.append(Paragraph("Exámenes recomendados:", styles["Heading2"]))
    for enf, lista in examenes.items():
        contenido.append(Paragraph(f"{enf}:", styles["Normal"]))
        for ex in lista:
            contenido.append(Paragraph(f"- {ex}", styles["Normal"]))

    doc.build(contenido)

    return ruta_pdf