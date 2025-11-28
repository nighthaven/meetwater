from uuid import UUID
from typing import Annotated
from fastapi import Depends
from src.models import get_db
from sqlalchemy.orm import Session
from src.models.swimming_coach import SwimmingCoach


class SwimmingCoachRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def save(self, swimming_coach: SwimmingCoach):
        try:
            self.db.add(swimming_coach)
            self.db.commit()
            self.db.refresh(swimming_coach)
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def get(self, swimming_coach_id: UUID) -> SwimmingCoach | None:
        try:
            return (
                self.db.query(SwimmingCoach)
                .filter_by(id=swimming_coach_id)
                .one_or_none()
            )
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e
