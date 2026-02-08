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
from src.routes.dto.booking.booking_with_swimmer_response_model import (
    BookingWithSwimmersResponseModel,
)
from src.routes.dto.coach_pack.coach_pack_response_model import CoachPackResponseModel
from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel
from src.routes.dto.swimming_coach.coach_schedule_response_model import (
    CoachScheduleResponseModel,
)
from src.routes.dto.swimming_coach.swimming_coach_query import SwimmingCoachQuery
from src.routes.dto.swimming_coach.swimming_coach_with_swimmers_and_schedule_response_model import (
    SwimmingCoachWithBookingsAndSwimmersAndSchedulesResponseModel,
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
    response_model=SwimmingCoachWithBookingsAndSwimmersAndSchedulesResponseModel,
)
def get_swimming_coach(
    swimming_coach_id: UUID,
    swimming_coach_repository: Annotated[Any, Depends(SwimmingCoachRepository)],
    current_swimming_coach: SwimmingCoach = Depends(
        Security.get_current_swimming_coach
    ),
):
    try:
        coach = get_swimming_coach_by_id(
            swimming_coach_id, swimming_coach_repository, current_swimming_coach
        )
        return SwimmingCoachWithBookingsAndSwimmersAndSchedulesResponseModel(
            id=coach.id,
            first_name=coach.first_name,
            last_name=coach.last_name,
            schedules=[
                CoachScheduleResponseModel(
                    id=schedule.id,
                    activity=schedule.activity,
                    scheduled_at=schedule.scheduled_at,
                    duration_minutes=schedule.duration_minutes,
                )
                for schedule in coach.schedules
            ],
            students=[
                SwimmerResponseModel(
                    id=swimmer.id,
                    first_name=swimmer.first_name,
                    last_name=swimmer.last_name,
                    birth_date=swimmer.birth_date,
                    level=swimmer.level,
                )
                for swimmer in coach.students
            ],
            bookings=[
                BookingWithSwimmersResponseModel(
                    id=booking.id,
                    appointment_at=booking.appointment_at,
                    created_at=booking.created_at,
                    duration_minutes=booking.duration_minutes,
                    status=booking.status,
                    swimming_coach_name=booking.swimming_coach.full_name,
                    swimmers=[
                        SwimmerResponseModel.model_validate(sb.swimmer)
                        for sb in booking.swimmers
                    ],
                )
                for booking in coach.bookings
            ],
            coach_packs=[
                CoachPackResponseModel(
                    id=pack.id,
                    sessions_count=pack.sessions_count,
                    price=pack.price,
                    final_price=pack.final_price,
                    active=pack.active,
                )
                for pack in coach.coach_packs
            ],
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
