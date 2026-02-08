from typing import List

from src.routes.dto.booking.booking_with_swimmer_response_model import (
    BookingWithSwimmersResponseModel,
)
from src.routes.dto.coach_pack.coach_pack_response_model import CoachPackResponseModel
from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel
from src.routes.dto.swimming_coach.coach_schedule_response_model import (
    CoachScheduleResponseModel,
)
from src.routes.dto.swimming_coach.swimming_coach_response_model import (
    SwimmingCoachResponseModel,
)


class SwimmingCoachWithBookingsAndSwimmersAndSchedulesResponseModel(
    SwimmingCoachResponseModel
):
    schedules: List[CoachScheduleResponseModel]
    students: List[SwimmerResponseModel]
    bookings: List[BookingWithSwimmersResponseModel]
    coach_packs: List[CoachPackResponseModel]
