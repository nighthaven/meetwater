from uuid import UUID
from typing import Annotated, Any

from fastapi import APIRouter, Depends, status, HTTPException

from src.exceptions.pool_manager.pool_manager_not_found_exception import (
    PoolManagerNotFoundException,
)
from src.exceptions.swimming_coach.swimming_coach_not_current_coach import (
    SwimmingCoachNotCurrentCoach,
)
from src.exceptions.swimming_coach.swimming_coach_not_found_exception import (
    SwimmingCoachNotFoundException,
)
from src.models.pool_manager import PoolManager
from src.models.swimming_coach import SwimmingCoach
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.repositories.swimming_pool_repository import SwimmingPoolRepository
from src.routes.dto.swimming_coach.swimming_coach_query import SwimmingCoachQuery
from src.routes.dto.swimming_coach.swimming_coach_with_schedule_response_model import (
    SwimmingCoachWithScheduleResponseModel,
)
from src.services.security import Security
from src.usecases.swimming_coach.create_swimming_coach import (
    create_swimming_coach_usecase,
)
from src.usecases.swimming_coach.get_swimming_coach_by_id import (
    get_swimming_coach_by_id,
)

router = APIRouter(
    prefix="/swimming_coaches",
    tags=["swimming_coaches"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_swimming_coach(
    query: SwimmingCoachQuery,
    security: Annotated[Any, Depends(Security)],
    swimming_pool_repository: Annotated[Any, Depends(SwimmingPoolRepository)],
    swimming_coach_repository: Annotated[Any, Depends(SwimmingCoachRepository)],
    current_pool_manager: PoolManager = Depends(Security.get_current_pool_manager),
):
    try:
        create_swimming_coach_usecase(
            query,
            security,
            swimming_pool_repository,
            swimming_coach_repository,
            current_pool_manager,
        )
    except PoolManagerNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not a pool manager"
        )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=SwimmingCoachWithScheduleResponseModel,
)
def get_swimming_coaches(
    swimming_coach_id: UUID,
    swimming_coach_repository: Annotated[Any, Depends(SwimmingCoachRepository)],
    current_swimming_coach: SwimmingCoach = Depends(
        Security.get_current_swimming_coach
    ),
):
    try:
        return get_swimming_coach_by_id(
            swimming_coach_id, swimming_coach_repository, current_swimming_coach
        )
    except SwimmingCoachNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Swimming coach not found"
        )
    except SwimmingCoachNotCurrentCoach:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User try to access other swimming coach information",
        )
