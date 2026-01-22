from datetime import datetime, timedelta

from src.exceptions.coach_schedule.a_schedule_is_already_existing_at_this_time_exception import (
    AScheduleIsAlreadyExistingAtThisTimeException,
)
from src.models.coach_schedule import CoachSchedule
from src.models.swimming_coach import SwimmingCoach
from src.repositories.coach_schedule_repository import CoachScheduleRepository


def create_coach_schedule_usecase(
    query, coach: SwimmingCoach, coach_schedule_repository: CoachScheduleRepository
):
    _check_if_schedule_exist(query.scheduled_at, coach)

    coach_schedule = CoachSchedule()
    coach_schedule.activity = query.activity
    coach_schedule.scheduled_at = query.scheduled_at
    coach_schedule.duration_minutes = query.duration_minutes
    coach_schedule.swimming_coach_id = coach.id
    coach_schedule_repository.save(coach_schedule)
    return


def _check_if_schedule_exist(scheduled_at: datetime, coach: SwimmingCoach):
    for schedule in coach.schedules:
        schedule_end = schedule.scheduled_at + timedelta(
            minutes=schedule.duration_minutes
        )
        if schedule.scheduled_at <= scheduled_at < schedule_end:
            raise AScheduleIsAlreadyExistingAtThisTimeException(
                "a schedule already exist"
            )
    return False
