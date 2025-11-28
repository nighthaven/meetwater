import uuid
from datetime import date, datetime

from sqlalchemy import (
    String,
    func,
    Date,
    CheckConstraint,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models import Base
from src.models.link.swimmer_representative import SwimmerRepresentative

from src.models.user import User


class Representative(Base):
    __tablename__ = "representatives"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True
    )
    user: Mapped["User"] = relationship(
        "User", uselist=False, cascade="all, delete-orphan", single_parent=True
    )
    swimmers: Mapped[list["SwimmerRepresentative"]] = relationship(
        "SwimmerRepresentative",
        back_populates="representative",
        cascade="all, delete-orphan",
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

    __table_args__ = (
        CheckConstraint(
            "birth_date <= current_date - interval '18 years'",
            name="check_minimum_age_18",
        ),
    )

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        email: str,
        password: str,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

        self.user = User(email=email, password=password)  # type: ignore[call-arg]

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
