from uuid import UUID
from typing import Annotated, Optional, cast
from fastapi import Depends
from sqlalchemy.orm import Session
from src.models import get_db
from src.models.coach_schedule import CoachSchedule


class CoachScheduleRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def save(self, coach_schedule: CoachSchedule):
        try:
            self.db.add(coach_schedule)
            self.db.commit()
            self.db.refresh(coach_schedule)
        except Exception as e:
            raise e

    def get(self):
        try:
            return self.db.query(CoachSchedule).all()
        except Exception as e:
            raise e

    def find(self, coach_schedule_id: UUID) -> Optional[CoachSchedule]:
        result = (
            self.db.query(CoachSchedule).filter_by(id=coach_schedule_id).one_or_none()
        )
        return cast(Optional[CoachSchedule], result)

    def delete(self, coach_schedule_id: UUID):
        self.db.query(CoachSchedule).filter_by(id=coach_schedule_id).delete()
        self.db.commit()
        return
