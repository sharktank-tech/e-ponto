from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def enviar_email(destinatario, assunto, corpo):
    servidor_smtp = "smtp.gmail.com"
    porta_smtp = 587
    remetente = "quicknotes527@gmail.com"
    senha = "qmlf rluh ixum tldt"  # Use uma senha de aplicativo em vez da senha da conta principal

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

    # Alterar o tipo para 'html' para permitir conteúdo formatado
    msg.attach(MIMEText(corpo, 'html'))

    try:
        with smtplib.SMTP(servidor_smtp, porta_smtp) as server:
            server.starttls()  # Inicializa a comunicação segura
            server.login(remetente, senha)
            server.send_message(msg)
            print(f"E-mail enviado para {destinatario} com sucesso!")
    except Exception as e:
        raise RuntimeError(f"Erro ao enviar e-mail: {e}")
