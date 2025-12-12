import factory
from datetime import timezone

from src.models.coach_schedule import CoachSchedule
from src.models.enums.coach_activity import CoachActivity
from src.services.date_time_service import DateTimeService


class CoachScheduleFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = CoachSchedule
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    activity = CoachActivity.AVAILABLE
    scheduled_at = factory.LazyFunction(
        lambda: DateTimeService.futur_date_and_time(1, 14).astimezone(timezone.utc)
    )
    duration_minutes = 30
    swimming_coach = factory.SubFactory(
        "tests.fixtures.swimming_coach_factory.SwimmingCoachFactory"
    )
