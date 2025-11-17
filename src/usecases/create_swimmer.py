from src.exceptions.user.user_not_found_exception import UserNotFoundException
from src.models.link.swimmer_user_link import SwimmerUserLink
from src.models.swimmer import Swimmer
from src.repository.user_repository import UserRepository
from uuid import UUID


def create_swimmer_by_user_id(user_id: UUID, query, user_repository: UserRepository):
    user = user_repository.get_by_id(user_id)
    if not user:
        raise UserNotFoundException("User not found")
    swimmer = Swimmer()
    swimmer.first_name = query.first_name
    swimmer.last_name = query.last_name
    swimmer.birth_date = query.birth_date
    swimmer.level = query.level

    link = SwimmerUserLink(user=user, swimmer=swimmer)
    user_repository.save_swimmer_by_user_id(swimmer, link)
    return
