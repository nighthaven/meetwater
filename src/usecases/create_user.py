from src.models.user import User
from src.repository.user_repository import UserRepository
from typing import Annotated, Any
from fastapi import Depends


def create_user(user_query, user_repository: UserRepository) -> None:
    new_user = User(
        email=user_query.email,
        password=user_query.password,
        first_name=user_query.first_name,
        last_name=user_query.last_name,
        birth_date=user_query.birth_date,
        level=user_query.level,
        representative=user_query.representative,
    )
    user_repository.save(new_user)
    return

