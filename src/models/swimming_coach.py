import uuid
from typing import List, TYPE_CHECKING
from datetime import date, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Date, CheckConstraint, ForeignKey
from src.models import Base
from src.models.booking import Booking

if TYPE_CHECKING:
    from src.models.user import User


class SwimmingCoach(Base):
    __tablename__ = "swimming_coach"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    user: Mapped["User"] = relationship("User", back_populates="swimming_coach")
    bookings: Mapped[List["Booking"]] = relationship(
        "Booking", back_populates="swimming_coach", cascade="all, delete-orphan"
    )

    last_caep_certification_date: Mapped[date] = mapped_column(Date, nullable=True)
    last_pse_certification_date: Mapped[date] = mapped_column(Date, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "last_caep_certification_date IS NULL OR last_caep_certification_date >= current_date - interval '5 years'",
            name="check_last_caep_certification_date",
        ),
        CheckConstraint(
            "last_pse_certification_date IS NULL OR last_pse_certification_date >= current_date - interval '1 year'",
            name="check_last_pse_certification_date",
        ),
    )

    @validates("last_caep_certification_date")
    def validate_caep(self, key, value):
        caep_valid_time_days = 5 * 365
        if value and value < date.today() - timedelta(days=caep_valid_time_days):
            raise ValueError("CAEP certification expired")
        return value

    @validates("last_pse_certification_date")
    def validate_pse(self, key, value):
        pse_valid_time_days = 365
        if value and value < date.today() - timedelta(days=pse_valid_time_days):
            raise ValueError("PSE certification expired")
        return value
