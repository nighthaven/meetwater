from fastapi import HTTPException
from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, status

from src.exceptions.representative.representative_not_found_exception import (
    RepresentativeNotFoundException,
)
from src.models.representative import Representative
from src.repositories.representative_repository import RepresentativeRepository
from src.repositories.swimmer_repository import SwimmerRepository
from src.routes.dto.swimmer.swimmer_query import SwimmerQuery
from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel
from src.services.security import Security
from src.usecases.swimmers.create_swimmer import create_swimmer_usecase
from src.usecases.swimmers.get_swimmers_by_representative import (
    get_swimmers_by_representative,
)

router = APIRouter(
    prefix="/swimmers",
    tags=["swimmers"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_swimmer(
    query: SwimmerQuery,
    representative_repository: Annotated[Any, Depends(RepresentativeRepository)],
    swimmer_repository: Annotated[Any, Depends(SwimmerRepository)],
    current_representative: Representative = Depends(
        Security.get_current_representative
    ),
):
    try:
        create_swimmer_usecase(
            query, representative_repository, swimmer_repository, current_representative
        )
        return None
    except RepresentativeNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Swimmer not found"
        )


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[SwimmerResponseModel]
)
def get_swimmers(
    swimmer_repository: Annotated[Any, Depends(SwimmerRepository)],
    current_representative: Representative = Depends(
        Security.get_current_representative
    ),
):
    try:
        swimmers = get_swimmers_by_representative(
            swimmer_repository, current_representative
        )
        return swimmers
    except RepresentativeNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Swimmer not found"
        )
