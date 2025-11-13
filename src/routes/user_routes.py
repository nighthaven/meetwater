from typing import Annotated, Any

from src.models.user import User
from src.repository.user_repository import UserRepository
from src.routes.dto.user.user_query import UserQuery

from fastapi import APIRouter, status

from src.usecases.create_user import create_user
from src.utils.security import Security
from fastapi import Depends

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user_route(
        query: UserQuery,
        crypto: Annotated[Any, Depends(Security)],
        user_repository: Annotated[Any, Depends(UserRepository)]
):
    new_user = User(
        email=query.email,
        password=crypto.hash_password(query.password),
        first_name=query.first_name,
        last_name=query.last_name,
        birth_date=query.birth_date,
        representative=query.representative,
    )
    create_user(new_user, user_repository)
    return

