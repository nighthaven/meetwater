import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from src.models import Base
from sqlalchemy import ForeignKey, Integer, TIMESTAMP, func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.models.enums.pack_status import PackStatus


class UserPack(Base):
    __tablename__ = "user_pack"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    representative_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("representatives.id"), nullable=False
    )
    swimming_coach_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("swimming_coaches.id"), nullable=False
    )
    sessions_total: Mapped[int] = mapped_column(Integer, nullable=False)
    sessions_remaining: Mapped[int] = mapped_column(Integer, nullable=False)
    price_paid: Mapped[float] = mapped_column(Integer, nullable=False)
    status: Mapped[PackStatus] = mapped_column(
        Enum(PackStatus, name="pack_status_enum"),
        default=PackStatus.PENDING,
        nullable=False,
    )
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
