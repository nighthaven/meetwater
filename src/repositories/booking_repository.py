from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from src.models import get_db
from src.models.booking import Booking
from src.models.link.swimmers_bookings import SwimmerBooking


class BookingRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def save(self, booking: Booking):
        try:
            self.db.add(booking)
            self.db.commit()
            self.db.refresh(booking)
        except Exception as e:
            raise e

    def get_all(self) -> List[Booking]:
        try:
            return self.db.query(Booking).all()
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def find(self, booking_id: UUID) -> Optional[Booking]:
        return self.db.query(Booking).filter_by(id=booking_id).one_or_none()

    def get_bookings_by_swimmers(self, swimmers_ids: List[UUID]) -> List[Booking]:
        subq = (
            self.db.query(SwimmerBooking.booking_id)
            .filter(SwimmerBooking.swimmer_id.in_(swimmers_ids))
            .distinct()
            .subquery()
        )

        bookings = (
            self.db.query(Booking)
            .options(joinedload(Booking.swimmers))
            .filter(Booking.id.in_(subq))  # type: ignore[arg-type]
            .all()
        )
        return bookings

    def delete(self, booking_id: UUID):
        return self.db.query(Booking).filter_by(id=booking_id).delete()
