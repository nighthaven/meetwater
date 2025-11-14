from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from src.repository.user_repository import UserRepository
from src.routes.dto.user.user_query import UserQuery
from src.services.security import Security
from src.usecases.create_user import create_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user_route(
    query: UserQuery,
    security: Annotated[Any, Depends(Security)],
    user_repository: Annotated[Any, Depends(UserRepository)],
):
    create_user(query, user_repository, security)
    return
