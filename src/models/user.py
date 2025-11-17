import uuid
from typing import TYPE_CHECKING, List
from datetime import datetime, date

from sqlalchemy import (
    TIMESTAMP,
    String,
    func,
    Date,
    CheckConstraint,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models import Base
from src.models.link.swimmer_user_link import SwimmerUserLink

if TYPE_CHECKING:
    from src.models.link.swimmer_user_link import SwimmerUserLink


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        server_default=func.now(),
        nullable=False,
    )
    swimmers: Mapped[List["SwimmerUserLink"]] = relationship(
        "SwimmerUserLink", back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "birth_date <= current_date - interval '18 years'",
            name="check_minimum_age_18",
        ),
    )

    @hybrid_property
    def age(self) -> int:
        today = date.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    @age.expression  # type: ignore[no-redef]
    def age(cls):
        return func.date_part("year", func.age(func.current_date(), cls.birth_date))

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
