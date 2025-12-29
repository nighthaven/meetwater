from fastapi import Depends

from src.models.link.swimmer_representative import SwimmerRepresentative
from src.models.representative import Representative
from src.models.swimmer import Swimmer
from src.repositories.representative_repository import RepresentativeRepository
from src.repositories.swimmer_repository import SwimmerRepository
from src.services.security import Security


def create_swimmer_usecase(
    query,
    representative_repository: RepresentativeRepository,
    swimmer_repository: SwimmerRepository,
    current_representative: Representative = Depends(
        Security.get_current_representative
    ),
):
    existing_swimmer = _get_swimmer_if_exist(
        query, representative_repository, swimmer_repository, current_representative
    )
    if not existing_swimmer:
        swimmer = Swimmer()
        swimmer.first_name = query.first_name
        swimmer.last_name = query.last_name
        swimmer.birth_date = query.birth_date
        swimmer.level = query.level

        link = SwimmerRepresentative(
            swimmer=swimmer, representative=current_representative
        )
        representative_repository.save_swimmer(swimmer, link)
    return


def _get_swimmer_if_exist(
    query,
    representative_repository: RepresentativeRepository,
    swimmer_repository: SwimmerRepository,
    current_representative: Representative,
) -> bool:
    swimmer_already_exist = swimmer_repository.get_by_name_and_birthdate(
        query.first_name, query.last_name, query.birth_date
    )
    if swimmer_already_exist:
        link = SwimmerRepresentative(
            swimmer=swimmer_already_exist, representative=current_representative
        )
        representative_repository.update_swimmer_representative(link)
        return True
    return False
