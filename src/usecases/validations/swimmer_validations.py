from uuid import UUID

from src.exceptions.swimmer.swimmer_not_found_exception import SwimmerNotFoundException
from src.repositories.swimmer_repository import SwimmerRepository


def validate_and_return_swimmer(
    swimmer_id: UUID, swimmer_repository: SwimmerRepository
):
    swimmer = swimmer_repository.find(swimmer_id)
    if not swimmer:
        raise SwimmerNotFoundException("Swimmer not found")
    return swimmer
