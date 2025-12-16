import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    func,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models import Base

from src.models.user import User

if TYPE_CHECKING:
    from src.models.swimming_pool import SwimmingPool


class PoolManager(Base):
    __tablename__ = "pool_manager"
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
    swimming_pool_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("swimming_pools.id"),
        nullable=False,
    )
    swimming_pool: Mapped["SwimmingPool"] = relationship(
        "SwimmingPool", back_populates="pool_managers"
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

    def __init__(
        self,
        first_name: str,
        last_name: str,
        swimming_pool_id: uuid.UUID,
        email: str,
        password: str,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.swimming_pool_id = swimming_pool_id

        self.user = User(email=email, password=password)  # type: ignore[call-arg]

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
