from uuid import UUID

from src.exceptions.coach_pack.coach_pack_do_not_belong_to_coach import (
    CoachPackDoNotBelongToCoach,
)
from src.models.swimming_coach import SwimmingCoach
from src.repositories.coach_pack_repository import CoachPackRepository


def delete_coach_pack_usecase(
    coach_pack_id: UUID,
    current_swimming_coach: SwimmingCoach,
    coach_pack_repository: CoachPackRepository,
):
    pack = [
        pack for pack in current_swimming_coach.coach_packs if pack.id == coach_pack_id
    ]
    if not pack:
        raise CoachPackDoNotBelongToCoach(
            "Coach pack do not belong to this coach of not found."
        )
    coach_pack_repository.delete(coach_pack_id)
    return
