from src.models.user import User
from src.repository.user_repository import UserRepository
from src.services.security import Security


def create_user(
    user_query, user_repository: UserRepository, security: Security
) -> None:
    new_user = User()
    new_user.email = user_query.email
    new_user.password = security.hash_password(user_query.password)
    new_user.first_name = user_query.first_name
    new_user.last_name = user_query.last_name
    new_user.birth_date = user_query.birth_date
    user_repository.save(new_user)
    return
