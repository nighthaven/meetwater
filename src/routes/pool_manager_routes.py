from typing import Annotated, Any

from fastapi import APIRouter, Depends, status, HTTPException

from src.exceptions.admin.admin_not_found_exception import AdminNotFoundException
from src.models.admin import Admin
from src.repositories.pool_manager_repository import PoolManagerRepository
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
    pool_manager_repository: Annotated[Any, Depends(PoolManagerRepository)],
    current_admin: Admin = Depends(Security.get_current_admin),
):
    try:
        create_pool_manager_usecase(
            query, security, pool_manager_repository, current_admin
        )
    except AdminNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user is not admin"
        )
    return
