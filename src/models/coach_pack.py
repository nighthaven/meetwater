import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from src.models import Base
from sqlalchemy import ForeignKey, Integer, Boolean, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column


class CoachPack(Base):
    __tablename__ = "coach_pack"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    swimming_coach_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("swimming_coaches.id"), nullable=False
    )
    sessions_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    price: Mapped[float] = mapped_column(Integer, nullable=False)
    final_price: Mapped[float] = mapped_column(Integer, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
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
