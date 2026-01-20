from uuid import UUID
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class BookingQuery(BaseModel):
    appointment_at: datetime
    duration_minutes: int = 30
    swimmers_ids: List[UUID]
    swimming_coach_id: Optional[UUID] = None
