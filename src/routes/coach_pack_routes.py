from fastapi import Depends, APIRouter, status
from typing import Annotated, Any
from src.models.swimming_coach import SwimmingCoach
from src.repositories.coach_pack_repository import CoachPackRepository
from src.routes.dto.coach_pack.coach_pack_query import CoachPackQuery
from src.services.security import Security
from src.usecases.coach_pack.create_coach_pack_usecase import create_coach_pack_usecase

router = APIRouter(
    prefix="/coach_pack",
    tags=["coach_pack"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_coach_pack(
    query: CoachPackQuery,
    coach_pack_repository: Annotated[Any, Depends(CoachPackRepository)],
    current_swimming_coach: SwimmingCoach = Depends(
        Security.get_current_swimming_coach
    ),
):
    return create_coach_pack_usecase(
        query, coach_pack_repository, current_swimming_coach
    )
