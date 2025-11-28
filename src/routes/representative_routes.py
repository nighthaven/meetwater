from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from src.repositories.representative_repository import RepresentativeRepository
from src.routes.dto.representative.query_representative import QueryRepresentative
from src.services.security import Security
from src.usecases.representative.create_representative import (
    create_representative_usecase,
)

router = APIRouter(
    prefix="/representatives",
    tags=["representatives"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_representative_user(
    query: QueryRepresentative,
    security: Annotated[Any, Depends(Security)],
    representative_repository: Annotated[Any, Depends(RepresentativeRepository)],
):
    create_representative_usecase(query, security, representative_repository)
    return
