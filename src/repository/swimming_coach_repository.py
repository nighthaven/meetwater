from uuid import UUID
from typing import Annotated
from fastapi import Depends
from src.models import get_db
from sqlalchemy.orm import Session
from src.models.swimming_coach import SwimmingCoach
from src.exceptions.unexpected_exception import UnexpectedException


class SwimmingCoachRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def get(self, swimming_coach_id: UUID) -> SwimmingCoach | None:
        try:
            return (
                self.db.query(SwimmingCoach)
                .filter_by(id=swimming_coach_id)
                .one_or_none()
            )
        except Exception:
            self.db.rollback()
            raise UnexpectedException(
                "Une erreur inattendu est arrivé, réessayez, si le problème persiste, n'hésitez pas à nous contacter"
            )
