import uuid
from typing import List, TYPE_CHECKING
from datetime import datetime, timezone

from src.exceptions.booking.booking_must_be_in_the_futur_exception import (
    BookingMustBeInTheFutureException,
)
from src.models.enums.booking_status import BookingStatus
from sqlalchemy.orm import validates

from sqlalchemy import DateTime, Enum, Integer, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.models.link.swimmers_bookings import SwimmerBooking


if TYPE_CHECKING:
    from src.models.swimming_coach import SwimmingCoach
    from src.models.swimmer import Swimmer


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    appointment_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, name="booking_status_enum"),
        default=BookingStatus.ACCEPTED,
        nullable=False,
    )
    swimmers: Mapped[List["SwimmerBooking"]] = relationship(
        "SwimmerBooking", back_populates="booking", cascade="all, delete-orphan"
    )
    students: Mapped[List["Swimmer"]] = relationship(
        "Swimmer", secondary="swimmers_bookings", viewonly=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    swimming_coach_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("swimming_coaches.id"), nullable=False
    )
    swimming_coach: Mapped["SwimmingCoach"] = relationship(
        "SwimmingCoach", back_populates="bookings"
    )
    user_pack_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_pack.id"), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "appointment_at > CURRENT_TIMESTAMP", name="ck_booking_booked_at_future"
        ),
    )

    @validates("appointment_at")
    def validate_appointment_at(self, key, value):
        if value <= datetime.now(tz=timezone.utc):
            raise BookingMustBeInTheFutureException("booked_at must be in the future.")
        return value
