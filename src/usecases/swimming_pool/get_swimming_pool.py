from fastapi import Request
from typing import Dict, Any

from src.exceptions.swimming_pool.swimming_pool_not_found_exception import (
    SwimmingPoolNotFoundException,
)
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.usecases.validations.swimming_pool_validations import (
    get_and_validate_swimming_pool_by_slug,
)


def get_swimming_pool_from_slug(
    request: Request, swimming_pool_repository: SwimmingPoolRepository
) -> Dict[str, Any]:
    slug = request.headers.get("subdomain")
    if not slug:
        raise SwimmingPoolNotFoundException("swimming pool not found")
    swimming_pool = get_and_validate_swimming_pool_by_slug(
        slug, swimming_pool_repository
    )
    coaches_schedules = [
        schedule for coach in swimming_pool.coaches for schedule in coach.schedules
    ]
    return {
        "pool_name": swimming_pool.pool_name,
        "slug": swimming_pool.slug,
        "address": swimming_pool.address,
        "city": swimming_pool.city,
        "post_code": swimming_pool.post_code,
        "schedules": swimming_pool.schedules,
        "coaches_schedules": coaches_schedules,
    }
