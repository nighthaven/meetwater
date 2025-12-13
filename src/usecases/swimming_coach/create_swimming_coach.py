from fastapi import Depends
from src.models.pool_manager import PoolManager
from src.models.swimming_coach import SwimmingCoach
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.routes.dto.swimming_coach.swimming_coach_query import SwimmingCoachQuery
from src.services.security import Security
from src.usecases.validations.swimming_pool_validations import (
    get_and_validate_swimming_pool,
)


def create_swimming_coach_usecase(
    swimming_coach_query: SwimmingCoachQuery,
    security: Security,
    swimming_pool_repository: SwimmingPoolRepository,
    swimming_coach_repository: SwimmingCoachRepository,
    current_pool_manager: PoolManager = Depends(Security.get_current_pool_manager),
):
    get_and_validate_swimming_pool(
        current_pool_manager.swimming_pool_id, swimming_pool_repository
    )
    swimming_coach = SwimmingCoach(
        first_name=swimming_coach_query.first_name,
        last_name=swimming_coach_query.last_name,
        last_caep_certification_date=swimming_coach_query.last_caep_certification_date,
        last_pse_certification_date=swimming_coach_query.last_pse_certification_date,
        swimming_pool_id=current_pool_manager.swimming_pool_id,
        email=swimming_coach_query.email,
        password=security.hash_password(swimming_coach_query.raw_password),
    )
    swimming_coach_repository.save(swimming_coach)
    return
