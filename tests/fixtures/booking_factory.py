import factory

from src.models.booking import Booking
from src.models.enums.booking_status import BookingStatus
from src.models.link.swimmers_bookings import SwimmerBooking
from src.services.date_time_service import DateTimeService
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory


class BookingFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = Booking
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    appointment_at = factory.LazyFunction(
        lambda: DateTimeService.futur_date_and_time(1, 14)
    )
    duration_minutes = 30
    status = BookingStatus.ACCEPTED
    swimming_coach = factory.SubFactory(SwimmingCoachFactory)

    @factory.post_generation
    def swimmers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for swimmer in extracted:
                SwimmerBookingFactory(swimmer=swimmer, booking=self)


class SwimmerBookingFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = SwimmerBooking
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    swimmer = None
    booking = None
