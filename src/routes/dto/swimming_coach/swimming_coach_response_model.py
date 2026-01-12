from pydantic import BaseModel
from typing import List
from uuid import UUID

from src.routes.dto.swimming_coach.coach_schedule_response_model import (
    CoachScheduleResponseModel,
)


class SwimmingCoachResponseModel(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    schedules: List[CoachScheduleResponseModel]
