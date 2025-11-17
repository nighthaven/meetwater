from src.exceptions.user.user_not_found_exception import UserNotFoundException
from src.repository.user_repository import UserRepository
from uuid import UUID

from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel
from src.routes.dto.user.user_response_model import UserResponseModel


def get_user_by_id_usecase(
    user_id: UUID,
    user_repository: UserRepository,
) -> UserResponseModel:
    user = user_repository.get_by_id(user_id)
    if not user:
        raise UserNotFoundException("User not found")
    swimmers_dto = [
        SwimmerResponseModel(
            first_name=link.swimmer.first_name,
            last_name=link.swimmer.last_name,
            birth_date=link.swimmer.birth_date,
            level=link.swimmer.level,
        )
        for link in user.swimmers
    ]

    return UserResponseModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        swimmers=swimmers_dto,
    )
