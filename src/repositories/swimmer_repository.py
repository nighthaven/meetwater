from uuid import UUID
from typing import Annotated, List

from src.models.link.swimmer_representative import SwimmerRepresentative
from src.models.swimmer import Swimmer
from datetime import date
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from src.models import get_db


class SwimmerRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def save(self, swimmer: Swimmer):
        try:
            self.db.add(swimmer)
            self.db.commit()
            self.db.refresh(swimmer)
        except Exception:
            self.db.rollback()
            self.db.close()
            raise

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

    def get_by_representative(self, representative_id: UUID) -> List[Swimmer]:
        try:
            return (
                self.db.query(Swimmer)
                .join(Swimmer.representatives)
                .filter(SwimmerRepresentative.representative_id == representative_id)
                .options(joinedload(Swimmer.representatives))
                .all()
            )
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
