from uuid import UUID

from src.exceptions.swimming_coach.swimming_coach_not_current_coach import (
    SwimmingCoachNotCurrentCoach,
)
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.usecases.validations.swimming_coach_validations import (
    get_and_validate_swimming_coach,
)


def get_swimming_coach_by_id(
    coach_id: UUID, swimming_coach_repository: SwimmingCoachRepository, current_coach
):
    coach = get_and_validate_swimming_coach(coach_id, swimming_coach_repository)
    if coach != current_coach:
        raise SwimmingCoachNotCurrentCoach()
    return coach
