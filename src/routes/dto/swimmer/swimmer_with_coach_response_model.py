from typing import List
from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel
from src.routes.dto.swimming_coach.swimming_coach_with_schedule_response_model import (
    SwimmingCoachWithScheduleResponseModel,
)


class SwimmerWithCoachAndSchedulesResponseModel(SwimmerResponseModel):
    coaches: List[SwimmingCoachWithScheduleResponseModel]
