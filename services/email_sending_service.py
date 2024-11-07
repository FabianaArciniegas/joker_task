import smtplib
from email.mime.text import MIMEText

from pydantic import EmailStr
from pyexpat.errors import messages

from core.config import settings


class EmailSendingService:
    def __init__(self):
        self.server = settings.SMTP_SERVER
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD

    async def send_email_to_reset_password(self, user_id: str, email: EmailStr, token: str) -> MIMEText:
        url = f'https://joker_task/reset-password/id={user_id}&token={token}'
        text_link = "Reset Password"
        text_message = f"Hacer click en el siguiente enlace: <a href='{url}'>{text_link}</a>"
        message = MIMEText(text_message, "html")
        message['Subject'] = "Reset Password"
        message['To'] = email
        await self._send_email(message)

    async def send_email_to_verify_user(self, user_id: str, email: EmailStr, token: str) -> MIMEText:
        url = f'https://joker_task/verify-user/id={user_id}&token={token}'
        text_link = "User verification"
        text_message = f"Hacer click en el siguiente enlace: <a href='{url}'>{text_link}</a>"
        message = MIMEText(text_message, "html")
        message['Subject'] = "User verification"
        message['To'] = email
        await self._send_email(message)

    async def _send_email(self, message: MIMEText):
        mailServer = smtplib.SMTP(self.server, self.port)
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.username, self.password)
        mailServer.sendmail(self.username, message['To'], message.as_string())
        mailServer.close()
