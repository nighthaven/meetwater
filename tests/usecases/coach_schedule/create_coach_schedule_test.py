from src.models.enums.coach_activity import CoachActivity
from src.routes.dto.coach_schedule.query_coach_schedule import QueryCoachSchedule
from src.services.date_time_service import DateTimeService
from src.usecases.coach_schedules.create_coach_schedule import (
    create_coach_schedule_usecase,
)
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory


class TestCreateCoachSchedule:
    def test_create_coach_schedule(self, coach_schedule_repo):
        swimming_coach = SwimmingCoachFactory()
        query = QueryCoachSchedule(
            activity=CoachActivity.AQUA_BIKE,
            scheduled_at=DateTimeService.futur_date_and_time(2, 14),
            duration_minutes=240,
        )

        create_coach_schedule_usecase(query, swimming_coach, coach_schedule_repo)

        query_schedules = coach_schedule_repo.get()
        assert len(query_schedules) == 1
        assert query_schedules[0].activity == swimming_coach.schedules[0].activity
        assert (
            query_schedules[0].scheduled_at == swimming_coach.schedules[0].scheduled_at
        )
        assert (
            query_schedules[0].duration_minutes
            == swimming_coach.schedules[0].duration_minutes
        )
