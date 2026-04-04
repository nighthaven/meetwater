from typing import Annotated
from fastapi import Depends
from src.models import get_db
from sqlalchemy.orm import Session

from src.models.admin import Admin


class AdminRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def find_by_user_id(self, user_id) -> Admin | None:
        return self.db.query(Admin).filter(Admin.user_id == user_id).first()

    def save(self, admin: Admin):
        try:
            self.db.add(admin)
            self.db.commit()
            self.db.refresh(admin)
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def count(self) -> int:
        return self.db.query(Admin).count()
