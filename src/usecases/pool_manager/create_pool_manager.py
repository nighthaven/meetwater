from fastapi import Depends

from src.exceptions.swimming_pool.swimming_pool_not_found_exception import (
    SwimmingPoolNotFoundException,
)
from src.models.admin import Admin
from src.models.pool_manager import PoolManager
from src.repositories.pool_manager_repository import PoolManagerRepository
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.routes.dto.pool_manager.pool_manager_query import PoolManagerQuery
from src.services.security import Security


def create_pool_manager_usecase(
    query: PoolManagerQuery,
    security: Security,
    swimming_pool_repository: SwimmingPoolRepository,
    pool_manager_repository: PoolManagerRepository,
    current_admin: Admin = Depends(Security.get_current_admin),
):
    swimming_pool = swimming_pool_repository.find(query.swimming_pool_id)
    if not swimming_pool:
        raise SwimmingPoolNotFoundException("swimming pool not found")
    pool_manager = PoolManager(
        first_name=query.first_name,
        last_name=query.last_name,
        swimming_pool_id=query.swimming_pool_id,
        email=query.email,
        password=security.hash_password(query.raw_password),
    )
    pool_manager_repository.save(pool_manager)
    return
