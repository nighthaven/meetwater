from uuid import UUID

from src.exceptions.coach_schedule.coach_schedule_not_found_exception import (
    CoachScheduleNotFoundException,
)
from src.models.coach_schedule import CoachSchedule
from src.repositories.coach_schedule_repository import CoachScheduleRepository


def get_and_validate_coach_schedule(
    coach_schedule_id: UUID,
    coach_schedule_repository: CoachScheduleRepository,
) -> CoachSchedule:
    coach_schedule = coach_schedule_repository.find(coach_schedule_id)
    if not coach_schedule:
        raise CoachScheduleNotFoundException("Coach schedule not found")
    return coach_schedule
