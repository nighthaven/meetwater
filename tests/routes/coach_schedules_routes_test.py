from datetime import timezone, datetime
from src.models.enums.coach_activity import CoachActivity
from src.services.date_time_service import DateTimeService
from tests.fixtures.coach_schedule_factory import CoachScheduleFactory


class TestCoachSchedulesRoutes:
    def test_create_coach_schedules_route(
        self, swimming_coach_client, coach_schedule_repo
    ):
        payload = {
            "activity": CoachActivity.AQUA_BIKE.value,
            "scheduled_at": DateTimeService.futur_date_and_time(1, 14).isoformat(),
            "duration_minutes": 240,
        }

        swimming_coach_client.post("/coach_schedules/", json=payload)

        query_coach_schedule = coach_schedule_repo.get()
        assert len(query_coach_schedule) == 1
        assert query_coach_schedule[0].activity == CoachActivity.AQUA_BIKE
        assert query_coach_schedule[0].scheduled_at == datetime.fromisoformat(
            payload["scheduled_at"]
        ).astimezone(timezone.utc)
        assert query_coach_schedule[0].duration_minutes == payload["duration_minutes"]

    def test_delete_coach_schedules_route(
        self, swimming_coach_client, coach_schedule_repo
    ):

        coach = swimming_coach_client.user_type
        coach_schedule = CoachScheduleFactory(swimming_coach=coach)

        response = swimming_coach_client.delete(
            f"/coach_schedules/{str(coach_schedule.id)}"
        )

        assert response.status_code == 204
