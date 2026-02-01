from uuid import UUID
from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi import Depends
from src.models import get_db
from src.models.link.swimmer_representative import SwimmerRepresentative
from src.models.representative import Representative
from src.models.swimmer import Swimmer


class RepresentativeRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def save(self, representative: Representative):
        try:
            self.db.add(representative)
            self.db.commit()
            self.db.refresh(representative)
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def get(self):
        try:
            return self.db.query(Representative).all()
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def find(self, representative_id) -> Representative | None:
        try:
            return (
                self.db.query(Representative)
                .filter(Representative.id == representative_id)
                .one_or_none()
            )
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def find_by_user_id(self, user_id: UUID) -> Representative | None:
        return (
            self.db.query(Representative)
            .filter(Representative.user_id == user_id)
            .one_or_none()
        )

    def save_swimmer(self, swimmer: Swimmer, link: SwimmerRepresentative):
        try:
            self.db.add(swimmer)
            self.db.add(link)
            self.db.commit()
            self.db.refresh(swimmer)
            self.db.refresh(link)
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def update_swimmer_representative(self, link: SwimmerRepresentative):
        try:
            self.db.add(link)
            self.db.commit()
            self.db.refresh(link)
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def get_swimmers(self, representative_id: UUID) -> List[Swimmer]:
        return (
            self.db.query(Swimmer)
            .join(SwimmerRepresentative, SwimmerRepresentative.swimmer_id == Swimmer.id)
            .filter(SwimmerRepresentative.representative_id == representative_id)
            .all()
        )
