from datetime import datetime

from pydantic import BaseModel

from src.models.enums.coach_activity import CoachActivity


class QueryCoachSchedule(BaseModel):
    activity: CoachActivity
    scheduled_at: datetime
    duration_minutes: int
