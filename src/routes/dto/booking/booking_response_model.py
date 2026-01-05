from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID

from src.models.enums.booking_status import BookingStatus
from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel
from datetime import datetime


class BookingResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    appointment_at: datetime
    created_at: datetime
    duration_minutes: int
    status: BookingStatus
    swimming_coach_name: str
    swimmers: List[SwimmerResponseModel]
