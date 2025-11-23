from typing import Annotated, List

from fastapi import Depends
from sqlalchemy.orm import Session
from src.models import get_db
from src.models.booking import Booking
from src.models.swimmer import Swimmer
from src.exceptions.unexpected_exception import UnexpectedException


class BookingRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def save(self, booking: Booking):
        try:
            self.db.add(booking)
            self.db.commit()
            self.db.refresh(booking)
        except Exception:
            self.db.rollback()
            raise UnexpectedException(
                "Une erreur inattendu est arrivé, réessayez, si le problème persiste, n'hésitez pas à nous contacter"
            )

    def get_all(self) -> List[Booking]:
        try:
            return self.db.query(Booking).all()
        except Exception:
            self.db.rollback()
            raise UnexpectedException(
                "Une erreur inattendu est arrivé, réessayez, si le problème persiste, n'hésitez pas à nous contacter"
            )

    def get_all_booking_by_swimmer(self, swimmer: Swimmer) -> List[Booking]:
        try:
            return self.db.query(Booking).filter(Booking.swimmers == swimmer).all()
        except Exception:
            self.db.rollback()
            raise UnexpectedException(
                "Une erreur inattendu est arrivé, réessayez, si le problème persiste, n'hésitez pas à nous contacter"
            )
