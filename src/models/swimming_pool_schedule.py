# src/models/swimming_pool_schedule.py
import uuid
from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum, Time, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]
from sqlalchemy.dialects.postgresql import UUID

from src.models import Base
from src.models.enums.day_of_week import DayOfWeek

if TYPE_CHECKING:
    from src.models.swimming_pool import SwimmingPool


class SwimmingPoolSchedule(Base):
    __tablename__ = "swimming_pool_schedules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    swimming_pool_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("swimming_pools.id", ondelete="CASCADE"),
        nullable=False,
    )
    day_of_week: Mapped[DayOfWeek] = mapped_column(SQLEnum(DayOfWeek), nullable=False)
    opening_time: Mapped[time] = mapped_column(Time, nullable=False)
    closing_time: Mapped[time] = mapped_column(Time, nullable=False)

    swimming_pool: Mapped["SwimmingPool"] = relationship(
        "SwimmingPool", back_populates="schedules"
    )

    __table_args__ = (
        CheckConstraint("closing_time > opening_time", name="ck_opening_closing_times"),
    )
