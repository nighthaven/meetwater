from typing import TYPE_CHECKING

from src.models import Base
import uuid
from datetime import datetime

from sqlalchemy import Enum, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models.enums.coach_activity import CoachActivity

if TYPE_CHECKING:
    from src.models.swimming_coach import SwimmingCoach


class CoachSchedule(Base):
    __tablename__ = "coaches_schedules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    activity: Mapped[CoachActivity] = mapped_column(
        Enum(CoachActivity, name="coach_activity"),
        default=CoachActivity.PUBLIC_LIFEGUARDING,
        nullable=False,
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    swimming_coach_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("swimming_coaches.id"),
    )
    swimming_coach: Mapped["SwimmingCoach"] = relationship(
        "SwimmingCoach", back_populates="schedules"
    )

    __init__ = Base.__init__
