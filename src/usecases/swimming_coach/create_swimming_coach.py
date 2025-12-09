from fastapi import Depends
from src.models.pool_manager import PoolManager
from src.models.swimming_coach import SwimmingCoach
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.routes.dto.swimming_coach.swimming_coach_query import SwimmingCoachQuery
from src.services.security import Security


def create_swimming_coach_usecase(
    swimming_coach_query: SwimmingCoachQuery,
    security: Security,
    swimming_coach_repository: SwimmingCoachRepository,
    current_pool_manager: PoolManager = Depends(Security.get_current_pool_manager),
):
    swimming_coach = SwimmingCoach(
        first_name=swimming_coach_query.first_name,
        last_name=swimming_coach_query.last_name,
        last_caep_certification_date=swimming_coach_query.last_caep_certification_date,
        last_pse_certification_date=swimming_coach_query.last_pse_certification_date,
        email=swimming_coach_query.email,
        password=security.hash_password(swimming_coach_query.raw_password),
    )
    swimming_coach_repository.save(swimming_coach)
    return
