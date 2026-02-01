from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from src.models import get_db
from src.models.user import User


class AuthRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def find(self, username: str):
        return self.db.query(User).filter(User.email == username).first()
