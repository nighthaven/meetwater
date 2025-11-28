from uuid import UUID

from src.exceptions.representative.representative_not_found_exception import (
    RepresentativeNotFoundException,
)
from src.repositories.representative_repository import RepresentativeRepository


def validate_and_return_representative(
    representative_id: UUID, representative_repository: RepresentativeRepository
):
    representative = representative_repository.find(representative_id)
    if not representative:
        raise RepresentativeNotFoundException("Representative not found")
    return representative
