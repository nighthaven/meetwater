from typing import Annotated, Any

from fastapi import APIRouter, Depends, status, HTTPException

from src.exceptions.admin.admin_not_found_exception import AdminNotFoundException
from src.exceptions.swimming_pool.swimming_pool_not_found_exception import (
    SwimmingPoolNotFoundException,
)
from src.models.admin import Admin
from src.repositories.pool_manager_repository import PoolManagerRepository
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.routes.dto.pool_manager.pool_manager_query import PoolManagerQuery
from src.services.security import Security
from src.usecases.pool_manager.create_pool_manager import create_pool_manager_usecase

router = APIRouter(
    prefix="/pool_managers",
    tags=["pool_managers"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_pool_manager_user(
    query: PoolManagerQuery,
    security: Annotated[Any, Depends(Security)],
    swimming_pool_repository: Annotated[Any, Depends(SwimmingPoolRepository)],
    pool_manager_repository: Annotated[Any, Depends(PoolManagerRepository)],
    current_admin: Admin = Depends(Security.get_current_admin),
):
    try:
        create_pool_manager_usecase(
            query,
            security,
            swimming_pool_repository,
            pool_manager_repository,
            current_admin,
        )
    except AdminNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user is not admin"
        )
    except SwimmingPoolNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="swimming pool not found"
        )
    return
