from datetime import datetime, timedelta
from typing import Any, Dict, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.config import settings
from src.models import get_db
from src.models.user import User
from src.routes.dto.auth.token_data import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORYTHM = settings.algorythm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)


class Security:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return cast(str, self.pwd_context.hash(password))

    def verify_password(self, plain_password: str, hashed_password: str | None) -> bool:
        return cast(bool, self.pwd_context.verify(plain_password, hashed_password))

    @staticmethod
    def create_access_token(data: Dict[str, Any]):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        try:
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORYTHM)
            return encoded_jwt
        except JWTError:
            return None

    @staticmethod
    def verify_access_token(token: str, credential_exception):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
            user_id = payload.get("user_id")
            if user_id is None:
                raise credential_exception
            token_data = TokenData(id=user_id)
        except JWTError:
            raise credential_exception
        return token_data

    def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credential",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data: TokenData = self.verify_access_token(token, credential_exception)
        user = db.query(User).filter_by(id=token_data.id).first()
        return user
