from src.models.coach_pack import CoachPack
from src.models.swimming_coach import SwimmingCoach
from src.repositories.coach_pack_repository import CoachPackRepository
from src.routes.dto.coach_pack.coach_pack_query import CoachPackQuery


def create_coach_pack_usecase(
    coach_pack_query: CoachPackQuery,
    coach_pack_repository: CoachPackRepository,
    current_swimming_coach: SwimmingCoach,
):

    coach_pack = CoachPack()
    coach_pack.swimming_coach_id = current_swimming_coach.id
    coach_pack.sessions_count = coach_pack_query.sessions_count
    coach_pack.price = coach_pack_query.price
    coach_pack.final_price = coach_pack_query.final_price
    coach_pack_repository.create(coach_pack)
    return
