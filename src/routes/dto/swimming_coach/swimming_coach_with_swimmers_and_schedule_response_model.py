from typing import List

from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel
from src.routes.dto.swimming_coach.coach_schedule_response_model import (
    CoachScheduleResponseModel,
)
from src.routes.dto.swimming_coach.swimming_coach_response_model import (
    SwimmingCoachResponseModel,
)


class SwimmingCoachWithSwimmerAndScheduleResponseModel(SwimmingCoachResponseModel):
    schedules: List[CoachScheduleResponseModel]
    students: List[SwimmerResponseModel]
