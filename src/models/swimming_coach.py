import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING
from datetime import date, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Date, CheckConstraint, ForeignKey, String, TIMESTAMP, func
from src.models import Base
from src.models.booking import Booking
from src.models.coach_schedule import CoachSchedule
from src.models.swimming_pool import SwimmingPool
from src.models.user import User

if TYPE_CHECKING:
    from src.models.link.swimmers_coachs import SwimmerCoach
    from src.models.swimmer import Swimmer


class SwimmingCoach(Base):
    __tablename__ = "swimming_coaches"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True
    )
    user: Mapped["User"] = relationship(
        "User", uselist=False, cascade="all, delete-orphan", single_parent=True
    )
    bookings: Mapped[List["Booking"]] = relationship(
        "Booking", back_populates="swimming_coach", cascade="all, delete-orphan"
    )
    swimmers: Mapped[List["SwimmerCoach"]] = relationship(
        "SwimmerCoach",
        back_populates="swimming_coach",
        cascade="all, delete-orphan",
    )
    students: Mapped[List["Swimmer"]] = relationship(
        "Swimmer", secondary="swimmers_coaches", viewonly=True
    )

    schedules: Mapped[List["CoachSchedule"]] = relationship(
        "CoachSchedule", back_populates="swimming_coach"
    )

    last_caep_certification_date: Mapped[date] = mapped_column(Date, nullable=True)
    last_pse_certification_date: Mapped[date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        server_default=func.now(),
        nullable=False,
    )
    swimming_pool_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("swimming_pool.id"),
        nullable=False,
    )

    swimming_pool: Mapped["SwimmingPool"] = relationship(
        "SwimmingPool", back_populates="coaches"
    )

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

    def __init__(
        self,
        first_name: str,
        last_name: str,
        last_caep_certification_date: date,
        last_pse_certification_date: date,
        swimming_pool_id: uuid.UUID,
        email: str,
        password: str,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.last_caep_certification_date = last_caep_certification_date
        self.last_pse_certification_date = last_pse_certification_date
        self.swimming_pool_id = swimming_pool_id

        self.user = User(email=email, password=password)  # type: ignore[call-arg]

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

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
