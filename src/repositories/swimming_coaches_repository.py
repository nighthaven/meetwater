from datetime import datetime, timedelta
from uuid import UUID
from typing import Annotated
from fastapi import Depends
from src.models import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from src.models.booking import Booking
from src.models.coach_schedule import CoachSchedule
from src.models.enums.coach_activity import CoachActivity
from src.models.swimming_coach import SwimmingCoach


class SwimmingCoachRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def save(self, swimming_coach: SwimmingCoach):
        try:
            self.db.add(swimming_coach)
            self.db.commit()
            self.db.refresh(swimming_coach)
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def get(self, swimming_coach_id: UUID) -> SwimmingCoach | None:
        try:
            return (
                self.db.query(SwimmingCoach)
                .options(joinedload(SwimmingCoach.schedules))
                .options(joinedload(SwimmingCoach.students))
                .options(
                    joinedload(SwimmingCoach.bookings).joinedload(Booking.swimmers)
                )
                .filter_by(id=swimming_coach_id)
                .one_or_none()
            )
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def find_by_user_id(self, user_id: UUID) -> SwimmingCoach | None:
        return self.db.query(SwimmingCoach).filter_by(user_id=user_id).one_or_none()

    def get_all_available_coach(
        self, appointment_at: datetime, duration: int, coach_planning: CoachActivity
    ) -> list[SwimmingCoach]:
        requested_start = appointment_at
        requested_end = appointment_at + timedelta(minutes=duration)

        query = (
            self.db.query(SwimmingCoach)
            .join(CoachSchedule)
            .filter(
                CoachSchedule.activity == coach_planning,
                CoachSchedule.scheduled_at <= requested_start,
                requested_end
                <= (
                    CoachSchedule.scheduled_at
                    + func.make_interval(
                        0, 0, 0, 0, 0, CoachSchedule.duration_minutes, 0
                    )
                ),
            )
            .outerjoin(Booking)
            .filter(
                (Booking.id.is_(None))
                | (
                    (
                        requested_start
                        >= (
                            Booking.appointment_at
                            + func.make_interval(
                                0, 0, 0, 0, 0, Booking.duration_minutes, 0
                            )
                        )
                    )
                    | ((Booking.appointment_at) >= requested_end)
                )
            )
            .options(joinedload(SwimmingCoach.schedules))
            .options(joinedload(SwimmingCoach.bookings))
            .distinct()
        )

        return query.all()
