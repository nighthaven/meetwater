from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from src.models import get_db
from src.models.coach_pack import CoachPack


class CoachPackRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create(self, coach_pack: CoachPack):
        try:
            self.db.add(coach_pack)
            self.db.commit()
            self.db.refresh(coach_pack)
            return
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def get(self):
        return self.db.query(CoachPack).all()
