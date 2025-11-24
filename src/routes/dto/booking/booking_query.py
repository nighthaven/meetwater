from uuid import UUID
from typing import List
from datetime import datetime

from pydantic import BaseModel


class BookingQuery(BaseModel):
    booked_at: datetime
    swimmers_ids: List[UUID]
    swimming_coach_id: UUID
