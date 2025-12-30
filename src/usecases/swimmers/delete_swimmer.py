from src.models.representative import Representative
from src.repositories.swimmer_repository import SwimmerRepository


def delete_swimmer_usecase(
    swimmer_id,
    swimmer_repository: SwimmerRepository,
    current_representative: Representative,
) -> None:
    swimmer = swimmer_repository.find(swimmer_id)

    if swimmer and swimmer.representatives:
        for swimmer_representative in swimmer.representatives:
            if swimmer_representative.representative == current_representative:
                swimmer_repository.delete_swimmer_representative(
                    swimmer_representative.id
                )
        if not swimmer.representatives:
            swimmer_repository.delete(swimmer_id)
    return
