from sqlalchemy.orm import Session
from typing import List

from src.models.coach_schedule import CoachSchedule
from src.models.enums.coach_activity import CoachActivity
from src.models.swimming_coach import SwimmingCoach
from src.services.date_time_service import DateTimeService


class CoachScheduleSeeds:
    def __init__(self, db: Session):
        self.db = db

    def create_coach_schedule(self, swimming_coaches: List[SwimmingCoach]) -> None:
        list_schedule_coach_without_swimmers = [
            CoachSchedule(
                activity=CoachActivity.PUBLIC_LIFEGUARDING,
                scheduled_at=DateTimeService.futur_date_and_time(1, 14),
                duration_minutes=60 * 4,
                swimming_coach_id=[
                    coach.id
                    for coach in swimming_coaches
                    if coach.full_name == "Bruce Wayne"
                ][0],
            ),
            CoachSchedule(
                activity=CoachActivity.AQUA_BIKE,
                scheduled_at=DateTimeService.futur_date_and_time(2, 14),
                duration_minutes=60 * 4,
                swimming_coach_id=[
                    coach.id
                    for coach in swimming_coaches
                    if coach.full_name == "Bruce Wayne"
                ][0],
            ),
            CoachSchedule(
                activity=CoachActivity.AVAILABLE,
                scheduled_at=DateTimeService.futur_date_and_time(3, 14),
                duration_minutes=60 * 4,
                swimming_coach_id=[
                    coach.id
                    for coach in swimming_coaches
                    if coach.full_name == "Bruce Wayne"
                ][0],
            ),
        ]

        # coach_with_swimmers
        for swimming_coach in swimming_coaches:
            if swimming_coach.full_name != "Bruce Wayne":
                list_schedule_coach_with_swimmers = [
                    CoachSchedule(
                        activity=CoachActivity.PUBLIC_LIFEGUARDING,
                        scheduled_at=DateTimeService.futur_date_and_time(1, 14),
                        duration_minutes=60 * 4,
                        swimming_coach_id=[
                            coach.id
                            for coach in swimming_coaches
                            if coach.full_name == swimming_coach.full_name
                        ][0],
                    ),
                    CoachSchedule(
                        activity=CoachActivity.AQUA_BIKE,
                        scheduled_at=DateTimeService.futur_date_and_time(2, 14),
                        duration_minutes=60 * 4,
                        swimming_coach_id=[
                            coach.id
                            for coach in swimming_coaches
                            if coach.full_name == swimming_coach.full_name
                        ][0],
                    ),
                    CoachSchedule(
                        activity=CoachActivity.AVAILABLE,
                        scheduled_at=DateTimeService.futur_date_and_time(3, 14),
                        duration_minutes=60 * 4,
                        swimming_coach_id=[
                            coach.id
                            for coach in swimming_coaches
                            if coach.full_name == swimming_coach.full_name
                        ][0],
                    ),
                ]
                self.db.add_all(list_schedule_coach_with_swimmers)

        self.db.add_all(list_schedule_coach_without_swimmers)
        self.db.flush()

        return
