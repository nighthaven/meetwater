from typing import List
from src.models.pool_manager import PoolManager
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from src.models import get_db


class PoolManagerRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def save(self, pool_manager: PoolManager):
        try:
            self.db.add(pool_manager)
            self.db.commit()
            self.db.refresh(pool_manager)
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def get(self) -> List[PoolManager]:
        try:
            return self.db.query(PoolManager).all()
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e
