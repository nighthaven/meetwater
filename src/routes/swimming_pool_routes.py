from fastapi import APIRouter, status, Request, Depends, HTTPException
from typing import Annotated, Any

from src.exceptions.representative.representative_not_found_exception import (
    RepresentativeNotFoundException,
)
from src.exceptions.swimming_pool.swimming_pool_not_found_exception import (
    SwimmingPoolNotFoundException,
)
from src.models.admin import Admin
from src.models.user import User
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.routes.dto.swimming_pool.swimming_pool_created_response_model import (
    SwimmingPoolCreatedResponseModel,
)
from src.routes.dto.swimming_pool.swimming_pool_query import SwimmingPoolQuery
from src.routes.dto.swimming_pool.swimming_pool_response_model import (
    SwimmingPoolResponseModel,
)
from src.services.security import Security
from src.usecases.swimming_pool.create_swimming_pool import create_swimming_pool_usecase
from src.usecases.swimming_pool.get_swimming_pool import get_swimming_pool_from_slug

router = APIRouter(
    prefix="/swimming_pool",
    tags=["swimming_pool"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SwimmingPoolCreatedResponseModel,
)
def create_swimming_pool(
    query: SwimmingPoolQuery,
    swimming_pool_repository: Annotated[Any, Depends(SwimmingPoolRepository)],
    current_admin: Admin = Depends(Security.get_current_admin),
):
    return create_swimming_pool_usecase(query, swimming_pool_repository)


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=SwimmingPoolResponseModel
)
def get_swimming_pool(
    request: Request,
    swimming_pool_repository: Annotated[Any, Depends(SwimmingPoolRepository)],
    current_user: User = Depends(Security.get_current_user),
):
    try:
        return get_swimming_pool_from_slug(request, swimming_pool_repository)
    except SwimmingPoolNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Swimming pool not found"
        )
    except RepresentativeNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not representative"
        )
