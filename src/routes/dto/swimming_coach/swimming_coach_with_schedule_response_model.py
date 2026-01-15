from typing import List
from src.routes.dto.swimming_coach.coach_schedule_response_model import (
    CoachScheduleResponseModel,
)
from src.routes.dto.swimming_coach.swimming_coach_response_model import (
    SwimmingCoachResponseModel,
)


class SwimmingCoachWithScheduleResponseModel(SwimmingCoachResponseModel):
    schedules: List[CoachScheduleResponseModel]
