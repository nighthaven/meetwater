from typing import Annotated, Any

from fastapi import APIRouter, Depends, status, HTTPException

from src.models.admin import Admin
from src.repositories.admin_repository import AdminRepository
from src.routes.dto.admin.admin_query import AdminQuery
from src.services.security import Security
from src.usecases.admin.create_admin import create_admin_usecase

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.post("/bootstrap", status_code=status.HTTP_201_CREATED)
def bootstrap_admin(
    query: AdminQuery,
    admin_repository: Annotated[Any, Depends(AdminRepository)],
):
    if admin_repository.count() > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An admin already exists",
        )
    create_admin_usecase(query, admin_repository)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_admin(
    query: AdminQuery,
    admin_repository: Annotated[Any, Depends(AdminRepository)],
    current_admin: Admin = Depends(Security.get_current_admin),
):
    create_admin_usecase(query, admin_repository)
