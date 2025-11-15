import uuid
from datetime import date, datetime

from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Date,
    Enum,
    String,
    and_,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped  # type: ignore[attr-defined]
from sqlalchemy.orm import mapped_column

from src.models import Base
from src.models.enums.user_level import UserLevel


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
    level: Mapped[UserLevel] = mapped_column(
        Enum(UserLevel, name="userlevel"),
        nullable=False,
        default=UserLevel.INTERMEDIATE,
    )
    representative: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date)) >= 5",
            name="user_minimum_age_check",
        ),
        CheckConstraint(
            "(EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date)) >= 18) OR representative IS NOT NULL",
            name="user_representative_if_minor_check",
        ),
    )

    @hybrid_property
    def has_representative_if_not_adult(self, legal_adult_age: int = 18) -> bool:
        return datetime.now().year - self.birth_date.year < legal_adult_age and bool(
            self.representative and self.representative.strip()
        )

    @has_representative_if_not_adult.expression  # type: ignore[no-redef]
    def has_representative_if_not_adult(cls):
        return and_(
            func.date_part("year", func.age(func.current_date(), cls.birth_date)) < 18,
            cls.representative is not None,
            func.length(func.trim(cls.representative)) > 0,
        )

    def full_name(self) -> str:
        return self.first_name + " " + self.last_name
