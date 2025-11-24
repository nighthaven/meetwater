import factory
from datetime import datetime, timedelta, timezone
import random

from src.models.booking import Booking
from src.models.enums.booking_status import BookingStatus
from src.models.link.swimmers_bookings_link import SwimmerBookingLink
from tests.fixtures.swimmer_factory import SwimmerFactory
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory


class BookingFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = Booking
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    booked_at = factory.LazyFunction(
        lambda: datetime.now(timezone.utc)
        + timedelta(days=1, minutes=random.choice([0, 30]))
    )
    time_slot = 30
    status = BookingStatus.ACCEPTED
    swimming_coach = factory.SubFactory(SwimmingCoachFactory)

    @factory.post_generation
    def swimmers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            swimmers = extracted if isinstance(extracted, list) else [extracted]
        else:
            return

        for swimmer in swimmers:
            SwimmerBookingLinkFactory(swimmer=swimmer, booking=self)


class SwimmerBookingLinkFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = SwimmerBookingLink
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    swimmer = factory.SubFactory(SwimmerFactory)
    booking = None
