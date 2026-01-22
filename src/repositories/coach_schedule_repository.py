from typing import Annotated
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
