from src.models.link.swimmer_user_link import SwimmerUserLink
from src.models.swimmer import Swimmer
from src.repository.user_repository import UserRepository
from uuid import UUID

from src.usecases.validations.user_validations import validate_and_return_user


def create_swimmer_by_user_id(user_id: UUID, query, user_repository: UserRepository):
    user = validate_and_return_user(user_id, user_repository)

    swimmer = Swimmer()
    swimmer.first_name = query.first_name
    swimmer.last_name = query.last_name
    swimmer.birth_date = query.birth_date
    swimmer.level = query.level

    link = SwimmerUserLink(user=user, swimmer=swimmer)
    user_repository.save_swimmer_by_user_id(swimmer, link)
    return
