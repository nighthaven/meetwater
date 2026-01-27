from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    TIMESTAMP,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models import Base

if TYPE_CHECKING:
    from src.models.representative import Representative
    from src.models.swimming_coach import SwimmingCoach
    from src.models.pool_manager import PoolManager
    from src.models.admin import Admin


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
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

    representative: Mapped[Representative | None] = relationship(  # type: ignore[name-defined]
        "Representative",
        back_populates="user",
        uselist=False,
    )

    swimming_coach: Mapped[SwimmingCoach | None] = relationship(  # type: ignore[name-defined]
        "SwimmingCoach",
        back_populates="user",
        uselist=False,
    )

    pool_manager: Mapped[PoolManager | None] = relationship(  # type: ignore[name-defined]
        "PoolManager",
        back_populates="user",
        uselist=False,
    )

    admin: Mapped[Admin | None] = relationship(  # type: ignore[name-defined]
        "Admin",
        back_populates="user",
        uselist=False,
    )
