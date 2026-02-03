from datetime import datetime
from src.exceptions.auth.invalid_credential_exception import InvalidCredentialException
from src.repositories.auth_repository import AuthRepository
from src.services.security import Security


def reset_password_usecase(
    raw_token: str,
    new_password: str,
    auth_repository: AuthRepository,
) -> None:
    security = Security()
    token_hash = security.hash_token(raw_token)

    reset_token = auth_repository.find_reset_token(token_hash)
    if not reset_token:
        raise InvalidCredentialException("Invalid token")
    if reset_token.used_at is not None:
        raise InvalidCredentialException("Token already used")
    if reset_token.expires_at < datetime.utcnow():
        raise InvalidCredentialException("Token expired")
    user = auth_repository.find_by_id(reset_token.user_id)
    if not user:
        raise InvalidCredentialException("User not found")
    hashed_password = security.hash_password(new_password)
    auth_repository.update_password(user, hashed_password)
    auth_repository.mark_reset_token_used(reset_token)
    return
