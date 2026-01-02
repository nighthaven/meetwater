from uuid import UUID

from src.exceptions.swimming_pool.swimming_pool_not_found_exception import (
    SwimmingPoolNotFoundException,
)
from src.models.swimming_pool import SwimmingPool
from src.repositories.swimming_pool_repository import SwimmingPoolRepository


def get_and_validate_swimming_pool(
    swimming_pool_id: UUID, swimming_pool_repository: SwimmingPoolRepository
) -> SwimmingPool:
    swimming_pool = swimming_pool_repository.find(swimming_pool_id)
    if not swimming_pool:
        raise SwimmingPoolNotFoundException("swimming pool not found")
    return swimming_pool


def get_and_validate_swimming_pool_by_slug(
    slug: str, swimming_pool_repository: SwimmingPoolRepository
) -> SwimmingPool:
    swimming_pool = swimming_pool_repository.find_by_slug(slug)
    if not swimming_pool:
        raise SwimmingPoolNotFoundException("swimming pool not found")
    return swimming_pool
