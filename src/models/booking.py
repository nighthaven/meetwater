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
from src.models.link.swimmers_bookings_link import SwimmerBookingLink

if TYPE_CHECKING:
    from src.models.swimming_coach import SwimmingCoach


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    booked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    time_slot: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, name="booking_status_enum"),
        default=BookingStatus.ACCEPTED,
        nullable=False,
    )
    swimmers: Mapped[List["SwimmerBookingLink"]] = relationship(
        "SwimmerBookingLink", back_populates="booking", cascade="all, delete-orphan"
    )
    swimming_coach_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("swimming_coach.id"), nullable=False
    )
    swimming_coach: Mapped["SwimmingCoach"] = relationship(
        "SwimmingCoach", back_populates="bookings"
    )

    __table_args__ = (
        CheckConstraint(
            "booked_at > CURRENT_TIMESTAMP", name="ck_booking_booked_at_future"
        ),
    )

    @validates("booked_at")
    def validate_booked_at(self, key, value):
        if value <= datetime.now(tz=timezone.utc):
            raise BookingMustBeInTheFutureException("booked_at must be in the future.")
        return value
