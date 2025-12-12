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
                .filter_by(id=swimming_coach_id)
                .one_or_none()
            )
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def get_all_available_coach(
        self, appointment_at: datetime, duration: int
    ) -> list[SwimmingCoach]:
        requested_start = appointment_at
        requested_end = appointment_at + timedelta(minutes=duration)

        query = (
            self.db.query(SwimmingCoach)
            .join(CoachSchedule)
            .filter(CoachSchedule.activity == CoachActivity.AVAILABLE)
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
