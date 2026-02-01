from typing import Dict
from datetime import datetime, timedelta
from src.models.password_reset_token import PasswordResetToken
from src.repositories.auth_repository import AuthRepository
from src.services.email_service import EmailService
from src.services.security import Security
import os


def request_password_reset_usecase(
    email: str,
    auth_repository: AuthRepository,
) -> Dict[str, str]:
    user = auth_repository.find(email)
    if not user:
        return {"message": "Si un compte existe, un email a été envoyé"}

    security = Security()
    raw_token, token_hash = security.generate_reset_token()

    reset_token = PasswordResetToken(  # type: ignore[call-arg]
        user_id=user.id,
        token_hash=token_hash,
        expires_at=datetime.utcnow() + timedelta(hours=1),
    )

    auth_repository.create_reset_token(reset_token)

    reset_link = f"{os.getenv('FRONTEND_BASE_URL')}/reset-password?token={raw_token}"

    EmailService().send_reset_email(user.email, reset_link)

    return {"message": "Si un compte existe, un email a été envoyé"}
