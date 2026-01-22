from uuid import UUID

from src.exceptions.swimming_coach.swimming_coach_not_current_coach import (
    SwimmingCoachNotCurrentCoach,
)
from src.models.coach_schedule import CoachSchedule
from src.models.swimming_coach import SwimmingCoach
from src.repositories.coach_schedule_repository import CoachScheduleRepository
from src.usecases.validations.get_and_validate_coach_schedule import (
    get_and_validate_coach_schedule,
)


def delete_coach_schedule_usecase(
    coach_schedule_id: UUID,
    current_coach: SwimmingCoach,
    coach_schedule_repository: CoachScheduleRepository,
):
    coach_schedule: CoachSchedule = get_and_validate_coach_schedule(
        coach_schedule_id, coach_schedule_repository
    )
    if coach_schedule.swimming_coach_id != current_coach.id:
        raise SwimmingCoachNotCurrentCoach(
            "Le planning n'appartient pas au coach souhaitant l'effacer."
        )
    coach_schedule_repository.delete(coach_schedule_id)
    return
