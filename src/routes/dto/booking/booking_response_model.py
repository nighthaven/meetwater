from pydantic import BaseModel, ConfigDict
from uuid import UUID

from src.models.enums.booking_status import BookingStatus
from datetime import datetime


class BookingResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    appointment_at: datetime
    created_at: datetime
    duration_minutes: int
    status: BookingStatus
    swimming_coach_name: str
