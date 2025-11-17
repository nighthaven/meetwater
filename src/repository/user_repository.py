from typing import Annotated, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from src.exceptions.unexpected_exception import UnexpectedException
from src.models import get_db
from src.models.user import User


class UserRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def save(self, user: User) -> None:
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except Exception:
            self.db.rollback()
            raise UnexpectedException(
                "une erreur inattendu est arrivé, réessayez, si le problème persiste, n'hésitez pas à nous contacter"
            )

    def get(self) -> List[User]:
        try:
            return self.db.query(User).all()
        except Exception:
            self.db.rollback()
            raise UnexpectedException(
                "Une erreur inattendu est arrivé, réessayez, si le problème persiste, n'hésitez pas à nous contacter"
            )

    def get_by_id(self, user_id: UUID) -> User | None:
        try:
            return (
                self.db.query(User)
                .filter_by(id=user_id)
                .options(joinedload(User.swimmers))
                .one_or_none()
            )
        except Exception:
            self.db.rollback()
            raise UnexpectedException(
                "Une erreur inattendu est arrivé, réessayez, si le problème persiste, n'hésitez pas à nous contacter"
            )
