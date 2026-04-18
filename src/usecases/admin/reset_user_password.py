from src.exceptions.user.user_not_found_exception import UserNotFoundException
from src.repositories.auth_repository import AuthRepository
from src.services.security import Security


def reset_user_password_usecase(
    email: str,
    new_password: str,
    auth_repository: AuthRepository,
) -> None:
    user = auth_repository.find(email)
    if not user:
        raise UserNotFoundException(f"No user found with email {email}")
    hashed_password = Security.hash_password(new_password)
    auth_repository.update_password(user, hashed_password)
