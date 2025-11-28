from fastapi import Depends
from src.models.admin import Admin
from src.models.pool_manager import PoolManager
from src.repositories.pool_manager_repository import PoolManagerRepository
from src.routes.dto.pool_manager.pool_manager_query import PoolManagerQuery
from src.services.security import Security


def create_pool_manager_usecase(
    query: PoolManagerQuery,
    security: Security,
    pool_manager_repository: PoolManagerRepository,
    current_admin: Admin = Depends(Security.get_current_admin),
):
    pool_manager = PoolManager(
        first_name=query.first_name,
        last_name=query.last_name,
        email=query.email,
        password=security.hash_password(query.raw_password),
    )
    pool_manager_repository.save(pool_manager)
    return
