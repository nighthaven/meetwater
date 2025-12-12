from uuid import UUID
from typing import Annotated
from fastapi import Depends
from src.models import get_db

from sqlalchemy.orm import Session

from src.models.swimming_pool import SwimmingPool


class SwimmingPoolRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def find(self, swimming_pool_id: UUID) -> SwimmingPool | None:
        return self.db.query(SwimmingPool).filter_by(id=swimming_pool_id).one_or_none()
