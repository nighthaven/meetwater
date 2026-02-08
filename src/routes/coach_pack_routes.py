from uuid import UUID
from fastapi import Depends, APIRouter, status, HTTPException
from typing import Annotated, Any

from src.exceptions.coach_pack.coach_pack_do_not_belong_to_coach import (
    CoachPackDoNotBelongToCoach,
)
from src.models.swimming_coach import SwimmingCoach
from src.repositories.coach_pack_repository import CoachPackRepository
from src.routes.dto.coach_pack.coach_pack_query import CoachPackQuery
from src.services.security import Security
from src.usecases.coach_pack.create_coach_pack_usecase import create_coach_pack_usecase
from src.usecases.coach_pack.delete_coach_pack_usecase import delete_coach_pack_usecase

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


@router.delete("/{coach_pack_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coach_pack(
    coach_pack_id: UUID,
    coach_pack_repository: Annotated[Any, Depends(CoachPackRepository)],
    current_swimming_coach: SwimmingCoach = Depends(
        Security.get_current_swimming_coach
    ),
):
    try:
        delete_coach_pack_usecase(
            coach_pack_id, current_swimming_coach, coach_pack_repository
        )
    except CoachPackDoNotBelongToCoach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coach pack do not belong to this coach of not found.",
        )
