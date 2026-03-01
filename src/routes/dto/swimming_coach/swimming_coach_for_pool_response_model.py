from uuid import UUID
from typing import List

from pydantic import BaseModel, ConfigDict

from src.routes.dto.swimming_coach.coach_schedule_response_model import (
    CoachScheduleResponseModel,
)


class SwimmingCoachForPoolResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    schedules: List[CoachScheduleResponseModel]
