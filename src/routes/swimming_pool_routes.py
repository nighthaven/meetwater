from fastapi import APIRouter, status, Request, Depends, HTTPException
from typing import Annotated, Any

from src.exceptions.representative.representative_not_found_exception import (
    RepresentativeNotFoundException,
)
from src.exceptions.swimming_pool.swimming_pool_not_found_exception import (
    SwimmingPoolNotFoundException,
)
from src.models.representative import Representative
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.services.security import Security
from src.usecases.swimming_pool.get_swimming_pool import get_swimming_pool_from_slug

router = APIRouter(
    prefix="/swimming_pool",
    tags=["swimming_pool"],
)


@router.get("/", status_code=status.HTTP_200_OK)
def get_swimming_pool(
    request: Request,
    swimming_pool_repository: Annotated[Any, Depends(SwimmingPoolRepository)],
    current_representative: Representative = Depends(
        Security.get_current_representative
    ),
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
