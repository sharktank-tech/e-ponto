from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def enviar_email(destinatario, assunto, corpo):
    servidor_smtp = "smtp.gmail.com"
    porta_smtp = 587
    remetente = "quicknotes527@gmail.com"
    senha = "qmlf rluh ixum tldt"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
            server.starttls()
            server.login(remetente, senha)
            server.send_message(msg)
    except Exception as e:
        raise RuntimeError(f"Erro ao enviar e-mail: {e}")