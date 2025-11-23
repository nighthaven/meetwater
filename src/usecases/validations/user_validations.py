from uuid import UUID

from src.exceptions.user.user_not_found_exception import UserNotFoundException
from src.repository.user_repository import UserRepository


def validate_and_return_user(user_id: UUID, user_repository: UserRepository):
    user = user_repository.get_by_id(user_id)
    if not user:
        raise UserNotFoundException("User not found")
    return user
