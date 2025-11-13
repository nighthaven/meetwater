import uuid
from datetime import datetime
from sqlalchemy import Date
from sqlalchemy.orm import (  # type: ignore[attr-defined]
    Mapped,
    mapped_column,
    relationship,
)
from typing import cast
from sqlalchemy.orm import validates
from sqlalchemy import func, and_

from sqlalchemy import ARRAY, TIMESTAMP, Column, Enum, String
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy import CheckConstraint

from src.exceptions.user.user_under_minimum_age_exception import UserUnderMinimumAgeException
from src.exceptions.user.user_without_representative_exception import UserWithoutRepresentativeException
from src.models import Base
from src.models.enums.user_level import UserLevel


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    level = mapped_column(
        cast(TypeEngine, ARRAY(Enum(UserLevel))),
        nullable=False,
        default=lambda: [UserLevel.INTERMEDIATE],
    )
    representative = Column(String, nullable=True)
    created_at = Column('created_at', TIMESTAMP(), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date)) >= 5", name="user_minimum_age_check"),
        CheckConstraint(
            "(EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date)) >= 18) OR representative IS NOT NULL",
            name="user_representative_if_minor_check"
        ),
    )

    @validates("birth_date", "representative")
    def validate_user(self, key, value):
        legal_adult_age = 18
        minimum_age = 5
        birth_date = self.birth_date if key != "birth_date" else value
        representative = self.representative if key != "representative" else value
        year_age = datetime.now().year - birth_date.year

        if key == "birth_date" and (year_age < minimum_age):
            raise UserUnderMinimumAgeException(f"User must be over {minimum_age} years old.")
        if year_age < legal_adult_age:
            if not representative or not representative.strip():
                raise UserWithoutRepresentativeException(f"User is under {legal_adult_age} and has no representative.")

        return value

    @hybrid_method
    def has_representative_if_not_adult(self, legal_adult_age: int = 18) -> bool:
        return datetime.now().year - self.birth_date.year < legal_adult_age and bool(
            self.representative and self.representative.strip())

    @has_representative_if_not_adult.expression
    def has_representative_if_not_adult(cls):
        return and_(
            func.date_part('year', func.age(func.current_date(), cls.birth_date)) < 18,
            cls.representative is not None,
            func.length(func.trim(cls.representative)) > 0
        )

    def full_name(self) -> str:
        return self.first_name + " " + self.last_name
