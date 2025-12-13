from uuid import UUID

from src.exceptions.swimming_pool.swimming_pool_not_found_exception import (
    SwimmingPoolNotFoundException,
)
from src.repositories.swimming_pool_repository import SwimmingPoolRepository


def get_and_validate_swimming_pool(
    swimming_pool_id: UUID, swimming_pool_repository: SwimmingPoolRepository
):
    swimming_pool = swimming_pool_repository.find(swimming_pool_id)
    if not swimming_pool:
        raise SwimmingPoolNotFoundException("swimming pool not found")
