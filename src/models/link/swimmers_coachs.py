import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models import Base
from src.models.swimming_coach import SwimmingCoach

if TYPE_CHECKING:
    from src.models.swimmer import Swimmer


class SwimmerCoach(Base):
    __tablename__ = "swimmers_coaches"
    swimmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("swimmers.id"), primary_key=True
    )
    swimming_coach_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("swimming_coaches.id"), primary_key=True
    )

    swimmer: Mapped["Swimmer"] = relationship(
        "Swimmer", back_populates="swimming_coaches"
    )
    swimming_coach: Mapped["SwimmingCoach"] = relationship(
        "SwimmingCoach", back_populates="swimmers"
    )
