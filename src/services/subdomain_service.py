from fastapi import Request, HTTPException, Depends

from src.models.swimming_pool import SwimmingPool
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.usecases.validations.swimming_pool_validations import (
    get_and_validate_swimming_pool_by_slug,
)


def get_swimming_pool_from_subdomain(
    request: Request,
    swimming_pool_repository: SwimmingPoolRepository = Depends(),
) -> SwimmingPool:
    subdomain = request.headers.get("subdomain")
    if not subdomain:
        raise HTTPException(400, "Host header missing")

    swimming_pool = get_and_validate_swimming_pool_by_slug(
        subdomain, swimming_pool_repository
    )
    return swimming_pool


def get_current_swimming_pool(
    request: Request,
    swimming_pool_repository: SwimmingPoolRepository = Depends(),
):
    return get_swimming_pool_from_subdomain(request, swimming_pool_repository)
