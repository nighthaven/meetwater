from typing import Annotated, Any

from fastapi import APIRouter, Depends, status, HTTPException

from src.exceptions.pool_manager.pool_manager_not_found_exception import (
    PoolManagerNotFoundException,
)
from src.models.pool_manager import PoolManager
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.routes.dto.swimming_coach.swimming_coach_query import SwimmingCoachQuery
from src.services.security import Security
from src.usecases.swimming_coach.create_swimming_coach import (
    create_swimming_coach_usecase,
)

router = APIRouter(
    prefix="/swimming_coaches",
    tags=["swimming_coaches"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_swimming_coach(
    query: SwimmingCoachQuery,
    security: Annotated[Any, Depends(Security)],
    swimming_coach_repository: Annotated[Any, Depends(SwimmingCoachRepository)],
    current_pool_manager: PoolManager = Depends(Security.get_current_pool_manager),
):
    try:
        create_swimming_coach_usecase(
            query, security, swimming_coach_repository, current_pool_manager
        )
    except PoolManagerNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not a pool manager"
        )
