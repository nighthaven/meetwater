import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[attr-defined]

from src.models import Base

if TYPE_CHECKING:
    from src.models.representative import Representative
    from src.models.swimmer import Swimmer


class SwimmerRepresentative(Base):
    __tablename__ = "swimmers_representatives"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    representative_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("representatives.id"), primary_key=True
    )
    swimmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("swimmers.id"), primary_key=True
    )

    representative: Mapped["Representative"] = relationship(
        "Representative", back_populates="swimmers"
    )
    swimmer: Mapped["Swimmer"] = relationship(
        "Swimmer", back_populates="representatives"
    )
