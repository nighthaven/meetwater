from uuid import UUID
from typing import Annotated
from src.models.swimmer import Swimmer
from src.exceptions.unexpected_exception import UnexpectedException
from sqlalchemy.orm import Session
from fastapi import Depends
from src.models import get_db


class SwimmerRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def get_swimmer_by_id(self, swimmer_id: UUID) -> Swimmer | None:
        try:
            return self.db.query(Swimmer).filter_by(id=swimmer_id).one_or_none()
        except Exception:
            self.db.rollback()
            raise UnexpectedException(
                "Une erreur inattendu est arrivé, réessayez, si le problème persiste, n'hésitez pas à nous contacter"
            )
