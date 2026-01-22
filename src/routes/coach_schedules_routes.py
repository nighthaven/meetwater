from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException

from typing import Annotated, Any

from src.exceptions.coach_schedule.a_schedule_is_already_existing_at_this_time_exception import (
    AScheduleIsAlreadyExistingAtThisTimeException,
)
from src.exceptions.coach_schedule.coach_schedule_not_found_exception import (
    CoachScheduleNotFoundException,
)
from src.exceptions.swimming_coach.swimming_coach_not_current_coach import (
    SwimmingCoachNotCurrentCoach,
)
from src.models.swimming_coach import SwimmingCoach
from src.repositories.coach_schedule_repository import CoachScheduleRepository
from src.routes.dto.coach_schedule.query_coach_schedule import QueryCoachSchedule
from src.services.security import Security
from src.usecases.coach_schedules.create_coach_schedule_usecase import (
    create_coach_schedule_usecase,
)
from src.usecases.coach_schedules.delete_coach_schedule_usecase import (
    delete_coach_schedule_usecase,
)

router = APIRouter(
    prefix="/coach_schedules",
    tags=["coach_schedules"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_coach_schedule(
    query: QueryCoachSchedule,
    coach_schedule_repository: Annotated[Any, Depends(CoachScheduleRepository)],
    current_swimming_coach: SwimmingCoach = Depends(
        Security.get_current_swimming_coach
    ),
):
    try:
        create_coach_schedule_usecase(
            query, current_swimming_coach, coach_schedule_repository
        )
    except AScheduleIsAlreadyExistingAtThisTimeException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A coach schedule already exists",
        )


@router.delete("/{coach_schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coach_schedule(
    coach_schedule_id: UUID,
    coach_schedule_repository: Annotated[Any, Depends(CoachScheduleRepository)],
    current_swimming_coach: SwimmingCoach = Depends(
        Security.get_current_swimming_coach
    ),
):
    try:
        delete_coach_schedule_usecase(
            coach_schedule_id, current_swimming_coach, coach_schedule_repository
        )
    except CoachScheduleNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Coach schedule not found"
        )
    except SwimmingCoachNotCurrentCoach:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Coach schedule not onwed by coach",
        )
