import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models import Base


if TYPE_CHECKING:
    from src.models.booking import Booking
    from src.models.swimmer import Swimmer


class SwimmerBooking(Base):
    __tablename__ = "swimmers_bookings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    swimmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("swimmers.id"), primary_key=True
    )
    booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("bookings.id"), primary_key=True
    )

    swimmer: Mapped["Swimmer"] = relationship("Swimmer", back_populates="bookings")
    booking: Mapped["Booking"] = relationship("Booking", back_populates="swimmers")
