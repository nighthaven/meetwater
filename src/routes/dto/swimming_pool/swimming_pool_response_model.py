from pydantic import BaseModel, ConfigDict
from typing import List

from src.routes.dto.swimming_coach.coach_schedule_response_model import (
    CoachScheduleResponseModel,
)
from src.routes.dto.swimming_pool.swimming_pool_schedule_response_model import (
    SwimmingPoolScheduleResponseModel,
)


class SwimmingPoolResponseModel(BaseModel):
    pool_name: str
    slug: str
    address: str
    city: str
    post_code: str
    schedules: List[SwimmingPoolScheduleResponseModel]
    coaches_schedules: List[CoachScheduleResponseModel]

    model_config = ConfigDict(from_attributes=True)
