from uuid import UUID
from typing import Annotated, List
from src.models.swimmer import Swimmer
from datetime import date
from sqlalchemy.orm import Session
from fastapi import Depends
from src.models import get_db


class SwimmerRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def get_by_name_and_birthdate(
        self, first_name: str, last_name: str, birthdate: date
    ) -> Swimmer | None:
        try:
            return (
                self.db.query(Swimmer)
                .filter(
                    Swimmer.first_name == first_name,
                    Swimmer.last_name == last_name,
                    Swimmer.birth_date == birthdate,
                )
                .one_or_none()
            )
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def get(self) -> List[Swimmer]:
        try:
            return self.db.query(Swimmer).all()
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def find(self, swimmer_id: UUID) -> Swimmer | None:
        try:
            return self.db.query(Swimmer).filter_by(id=swimmer_id).one_or_none()
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e
