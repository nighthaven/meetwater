import uuid
from typing import TYPE_CHECKING, List
from datetime import datetime, date
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy import (
    TIMESTAMP,
    Enum,
    String,
    func,
    Date,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models import Base
from src.models.enums.swimmer_level import SwimmerLevel

if TYPE_CHECKING:
    from src.models.link.swimmer_user_link import SwimmerUserLink


class Swimmer(Base):
    __tablename__ = "swimmers"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    level: Mapped[SwimmerLevel] = mapped_column(
        Enum(SwimmerLevel, name="userlevel"),
        nullable=False,
        default=SwimmerLevel.INTERMEDIATE,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        server_default=func.now(),
        nullable=False,
    )
    user_links: Mapped[List["SwimmerUserLink"]] = relationship(
        "SwimmerUserLink", back_populates="swimmer", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "birth_date <= current_date - interval '4 years'",
            name="check_minimum_age_4",
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

    def validate_age(self) -> None:
        min_birth_date = date.today().replace(year=date.today().year - 4)
        if self.birth_date > min_birth_date:
            raise ValueError("Le nageur doit avoir au moins 4 ans.")
