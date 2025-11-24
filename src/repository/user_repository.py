from typing import Annotated, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from src.exceptions.unexpected_exception import UnexpectedException
from src.models import get_db
from src.models.booking import Booking
from src.models.link.swimmer_user_link import SwimmerUserLink
from src.models.link.swimmers_bookings_link import SwimmerBookingLink
from src.models.swimmer import Swimmer
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
                .options(joinedload(User.swimming_coach))
                .one_or_none()
            )
        except Exception:
            self.db.rollback()
            raise UnexpectedException(
                "Une erreur inattendu est arrivé, réessayez, si le problème persiste, n'hésitez pas à nous contacter"
            )

    def save_swimmer_by_user_id(self, swimmer: Swimmer, link: SwimmerUserLink):
        try:
            self.db.add(swimmer)
            self.db.add(link)
            self.db.commit()
            self.db.refresh(swimmer)
            self.db.refresh(link)
        except Exception:
            self.db.rollback()
            raise UnexpectedException(
                "Une erreur inattendu est arrivé, réessayez, si le problème persiste, n'hésitez pas à nous contacter"
            )

    def get_swimmer_by_user_id(self, user_id: UUID) -> List[Swimmer]:
        return (
            self.db.query(Swimmer)
            .join(SwimmerUserLink, SwimmerUserLink.swimmer_id == Swimmer.id)
            .filter(SwimmerUserLink.user_id == user_id)
            .all()
        )

    def get_bookings(self, user_id: UUID) -> List[Booking]:
        try:
            bookings = (
                self.db.query(Booking)
                .join(Booking.swimmers)
                .join(SwimmerBookingLink.swimmer)
                .join(Swimmer.user_links)
                .filter(SwimmerUserLink.user_id == user_id)
                .options(
                    joinedload(Booking.swimmers).joinedload(SwimmerBookingLink.swimmer)
                )
                .all()
            )
            return bookings

        except Exception:
            self.db.rollback()
            raise UnexpectedException("Une erreur inattendu est arrivé...")
