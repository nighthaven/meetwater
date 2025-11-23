from pydantic import BaseModel
from typing import List

from src.models.enums.booking_status import BookingStatus
from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel
from datetime import datetime


class BookingDTO(BaseModel):
    booked_at: datetime
    created_at: datetime
    time_slot: int
    status: BookingStatus
    swimmers: List[SwimmerResponseModel]
