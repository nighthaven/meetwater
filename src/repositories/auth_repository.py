from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from src.models import get_db
from src.models.password_reset_token import PasswordResetToken
from src.models.user import User


class AuthRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def find(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_reset_token(self, token: PasswordResetToken):
        try:
            self.db.add(token)
            self.db.commit()
            return token
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e
