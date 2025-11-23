from src.repository.user_repository import UserRepository
from uuid import UUID
from typing import Dict, Any

from src.usecases.validations.user_validations import validate_and_return_user


def get_user_by_id_usecase(
    user_id: UUID,
    user_repository: UserRepository,
) -> Dict[str, Any]:
    user = validate_and_return_user(user_id, user_repository)

    swimmers = [
        {
            "first_name": link.swimmer.first_name,
            "last_name": link.swimmer.last_name,
            "birth_date": link.swimmer.birth_date,
            "level": link.swimmer.level,
        }
        for link in user.swimmers
    ]

    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "swimmers": swimmers,
    }
