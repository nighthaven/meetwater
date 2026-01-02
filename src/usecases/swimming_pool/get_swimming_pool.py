from fastapi import Request

from src.exceptions.swimming_pool.swimming_pool_not_found_exception import (
    SwimmingPoolNotFoundException,
)
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.usecases.validations.swimming_pool_validations import (
    get_and_validate_swimming_pool_by_slug,
)


def get_swimming_pool_from_slug(
    request: Request, swimming_pool_repository: SwimmingPoolRepository
):
    slug = request.headers.get("subdomain")
    if not slug:
        raise SwimmingPoolNotFoundException("swimming pool not found")
    return get_and_validate_swimming_pool_by_slug(slug, swimming_pool_repository)
