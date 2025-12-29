from fastapi import Request, HTTPException, Depends

from src.models.swimming_pool import SwimmingPool
from src.repositories.swimming_pool_repository import SwimmingPoolRepository


def get_swimming_pool_from_subdomain(
    request: Request,
    swimming_pool_repository: SwimmingPoolRepository = Depends(),
) -> SwimmingPool:
    host = request.headers.get("host")
    subdomain = host.split(".")[0] if host else None
    if not subdomain:
        raise HTTPException(400, "Host header missing")

    swimming_pool = swimming_pool_repository.find_by_slug(subdomain)
    if not swimming_pool:
        raise HTTPException(400, "Subdomain not found")
    return swimming_pool


def get_current_swimming_pool(
    request: Request,
    swimming_pool_repository: SwimmingPoolRepository = Depends(),
):
    return get_swimming_pool_from_subdomain(request, swimming_pool_repository)
