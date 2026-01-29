from fastapi import Depends
from typing import List, Annotated

from src.models.booking import Booking
from src.models.link.swimmers_bookings import SwimmerBooking
from src.models.representative import Representative
from src.models import get_db
from sqlalchemy.orm import Session
from src.services.date_time_service import DateTimeService


class BookingsSeeds:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def create_bookings_seeds(self, representatives: List[Representative]):
        list_created_bookings = []
        add_one_hour = 1
        for representative in representatives:
            for swimmer in representative.students:
                if swimmer.coaches:
                    booking_1 = Booking(  # type: ignore[call-arg]
                        appointment_at=DateTimeService.futur_date_and_time(
                            1, 13 + add_one_hour
                        ),
                        duration_minutes=30,
                        swimming_coach_id=swimmer.coaches[0].id,
                    )
                    booking_2 = Booking(  # type: ignore[call-arg]
                        appointment_at=DateTimeService.futur_date_and_time(
                            2, 13 + add_one_hour
                        ),
                        duration_minutes=30,
                        swimming_coach_id=swimmer.coaches[0].id,
                    )
                    self.db.add_all([booking_1, booking_2])
                    self.db.flush()

                    swimmer_booking_1 = SwimmerBooking(  # type: ignore[call-arg]
                        swimmer_id=swimmer.id,
                        booking_id=booking_1.id,
                    )
                    swimmer_booking_2 = SwimmerBooking(  # type: ignore[call-arg]
                        swimmer_id=swimmer.id,
                        booking_id=booking_2.id,
                    )
                    list_created_bookings.append(booking_1)
                    list_created_bookings.append(booking_2)
                    self.db.add_all([swimmer_booking_1, swimmer_booking_2])
                    self.db.flush()

                    add_one_hour = add_one_hour + 1
        return list_created_bookings
