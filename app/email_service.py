import smtplib
from email.message import EmailMessage
import os

def enviar_correo(destinatario, archivo_pdf):

    remitente = "yulianmaldonado1223@gmail.com"
    password = "lqir nrup isjk xnof"

    msg = EmailMessage()
    msg["Subject"] = "Reporte Médico"
    msg["From"] = remitente
    msg["To"] = destinatario

    msg.set_content("Adjunto encontrará su reporte clínico generado por el sistema.")

    # adjuntar PDF
    with open(archivo_pdf, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(archivo_pdf)

    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    # enviar
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, password)
        smtp.send_message(msg)