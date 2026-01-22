import pytest
from uuid import UUID

from src.exceptions.coach_schedule.coach_schedule_not_found_exception import (
    CoachScheduleNotFoundException,
)
from src.exceptions.swimming_coach.swimming_coach_not_current_coach import (
    SwimmingCoachNotCurrentCoach,
)
from src.usecases.coach_schedules.delete_coach_schedule_usecase import (
    delete_coach_schedule_usecase,
)
from tests.fixtures.coach_schedule_factory import CoachScheduleFactory
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory


class TestDeleteCoachSchedule:
    def test_delete_coach_schedule(self, coach_schedule_repo):
        coach_schedule = CoachScheduleFactory()

        delete_coach_schedule_usecase(
            coach_schedule.id, coach_schedule.swimming_coach, coach_schedule_repo
        )

        query_coach = coach_schedule_repo.get()
        assert len(query_coach) == 0

    def test_delete_coach_schedule_not_found(self, coach_schedule_repo):
        current_coach = SwimmingCoachFactory()

        with pytest.raises(CoachScheduleNotFoundException):
            delete_coach_schedule_usecase(
                UUID("f60ae389-8a53-4748-a238-529de5bb1451"),
                current_coach,
                coach_schedule_repo,
            )

    def test_delete_coach_schedule_different_coach_schedule(self, coach_schedule_repo):
        coach_schedule = CoachScheduleFactory()
        current_coach = SwimmingCoachFactory()

        with pytest.raises(SwimmingCoachNotCurrentCoach):
            delete_coach_schedule_usecase(
                coach_schedule.id, current_coach, coach_schedule_repo
            )
