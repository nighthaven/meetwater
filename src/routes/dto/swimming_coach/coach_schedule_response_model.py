from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from src.models.enums.coach_activity import CoachActivity


class CoachScheduleResponseModel(BaseModel):
    id: UUID
    activity: CoachActivity
    scheduled_at: datetime
    duration_minutes: int
