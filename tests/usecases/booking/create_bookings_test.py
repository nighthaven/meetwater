from datetime import datetime, timedelta, timezone

from src.models.booking import Booking
from src.routes.dto.booking.booking_query import BookingQuery
from src.usecases.booking.create_bookings import create_bookings_usecase
from tests.fixtures.swimmer_factory import SwimmerFactory
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory


class TestCreateBooking:
    def test_create_booking(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimmer = SwimmerFactory(representatives=[authenticated_representative])
        swimming_coach = SwimmingCoachFactory()
        date_appointement = datetime.now(timezone.utc) + timedelta(days=1)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer.id],
            swimming_coach_id=swimming_coach.id,
        )

        create_bookings_usecase(
            query,
            swimmer_repo,
            booking_repo,
            swimming_coach_repo,
            authenticated_representative,
        )

        query_booking = db_session.query(Booking).all()
        assert len(query_booking) == 1
        assert query_booking[0].appointment_at == date_appointement
        assert query_booking[0].swimmers[0].swimmer.id == swimmer.id
        assert query_booking[0].swimming_coach_id == swimming_coach.id
