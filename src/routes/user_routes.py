from fastapi import HTTPException
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.exceptions.user.user_not_found_exception import UserNotFoundException
from src.repository.user_repository import UserRepository
from src.routes.dto.user.user_query import UserQuery
from src.routes.dto.user.user_response_model import UserResponseModel
from src.services.security import Security
from src.usecases.create_user import create_user
from src.usecases.get_user import get_user_by_id

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


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseModel
)
def get_user_by_id_route(
    user_id: UUID,
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
):
    try:
        return get_user_by_id(user_id=user_id, user_repository=user_repository)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
