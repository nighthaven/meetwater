from uuid import UUID
from datetime import datetime
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

    def find_by_id(self, id: UUID):
        return self.db.query(User).filter(User.id == id).first()

    def create_reset_token(self, token: PasswordResetToken):
        try:
            self.db.add(token)
            self.db.commit()
            return token
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def find_reset_token(self, token_hash: str) -> PasswordResetToken | None:
        return (
            self.db.query(PasswordResetToken)
            .filter(PasswordResetToken.token_hash == token_hash)
            .first()
        )

    def update_password(self, user: User, hashed_password: str):
        try:
            user.password = hashed_password
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            self.db.close()
            raise e

    def mark_reset_token_used(self, reset_token: PasswordResetToken):
        reset_token.used_at = datetime.utcnow()
        self.db.commit()
