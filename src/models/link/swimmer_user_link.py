import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models import Base


if TYPE_CHECKING:
    from src.models.user import User
    from src.models.swimmer import Swimmer


class SwimmerUserLink(Base):
    __tablename__ = "swimmer_user_link"
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("users.id"), primary_key=True
    )
    swimmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("swimmers.id"), primary_key=True
    )

    user: Mapped["User"] = relationship("User", back_populates="swimmers")
    swimmer: Mapped["Swimmer"] = relationship("Swimmer", back_populates="user_links")
