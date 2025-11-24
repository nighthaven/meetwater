import factory
from datetime import datetime, timedelta, timezone
import random

from src.models.swimming_coach import SwimmingCoach
from tests.fixtures.user_factory import UserFactory


class SwimmingCoachFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = SwimmingCoach
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    user = factory.SubFactory(UserFactory)

    last_caep_certification_date = factory.LazyFunction(
        lambda: datetime.now(timezone.utc).date()
        - timedelta(days=random.randint(0, 5 * 365))
    )
    last_pse_certification_date = factory.LazyFunction(
        lambda: datetime.now(timezone.utc).date()
        - timedelta(days=random.randint(0, 365))
    )

    @factory.post_generation
    def bookings(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        bookings = extracted if isinstance(extracted, list) else [extracted]
        for booking in bookings:
            booking.swimming_coach = self
