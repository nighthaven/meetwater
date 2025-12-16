import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    func,
    TIMESTAMP,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models import Base
from src.models.pool_manager import PoolManager
from src.services.slugify import slugify

if TYPE_CHECKING:
    from src.models.swimming_coach import SwimmingCoach


class SwimmingPool(Base):
    __tablename__ = "swimming_pools"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    pool_name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    post_code: Mapped[str] = mapped_column(String, nullable=False)
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
    coaches: Mapped[list["SwimmingCoach"]] = relationship(
        "SwimmingCoach", back_populates="swimming_pool", cascade="all, delete-orphan"
    )
    pool_managers: Mapped[list["PoolManager"]] = relationship(
        "PoolManager", back_populates="swimming_pool", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "slug ~ '^[a-z0-9-]+$'",
            name="ck_swimming_pool_slug_format",
        ),
    )

    def __init__(self, pool_name, address, city, post_code) -> None:
        self.pool_name = pool_name
        self.address = address
        self.city = city
        self.post_code = post_code
        self.slug = slugify(pool_name)
