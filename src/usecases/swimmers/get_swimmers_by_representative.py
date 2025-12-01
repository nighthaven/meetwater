from src.models.representative import Representative
from src.repositories.swimmer_repository import SwimmerRepository


def get_swimmers_by_representative(
    swimmer_repository: SwimmerRepository, current_representative: Representative
):
    swimmers = swimmer_repository.get_by_representative(current_representative.id)
    return swimmers
