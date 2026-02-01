import os
import smtplib
from email.message import EmailMessage


class EmailService:
    def _send_email(self, to_email: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["From"] = os.getenv("FROM_EMAIL")
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        host = os.getenv("SMTP_HOST")
        port = os.getenv("SMTP_PORT")
        user = os.getenv("SMTP_USER")
        password = os.getenv("SMTP_PASSWORD")

        with smtplib.SMTP(host, port) as server:  # type: ignore[arg-type]
            server.starttls()
            server.login(user, password)  # type: ignore[arg-type]
            server.send_message(msg)

    def send_reset_email(self, email: str, link: str):
        subject = "Réinitialisation de votre mot de passe"
        body = f"""
        Bonjour,

        Cliquez sur le lien suivant pour réinitialiser votre mot de passe :
        {link}

        Ce lien est valable 1 heure.
        """
        self._send_email(email, subject, body)
