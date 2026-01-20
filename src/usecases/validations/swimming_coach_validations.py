from uuid import UUID

from src.exceptions.swimming_coach.swimming_coach_not_found_exception import (
    SwimmingCoachNotFoundException,
)
from src.models.swimming_coach import SwimmingCoach
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository


def get_and_validate_swimming_coach(
    swimming_coach_id: UUID, swimming_coach_repository: SwimmingCoachRepository
) -> SwimmingCoach:
    swimming_coach = swimming_coach_repository.get(swimming_coach_id)
    if not swimming_coach:
        raise SwimmingCoachNotFoundException("Swimming Coach not found")
    return swimming_coach
