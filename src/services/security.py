import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, cast
from sqlalchemy.orm import Session

from src.exceptions.admin.admin_not_found_exception import AdminNotFoundException
from src.exceptions.pool_manager.pool_manager_not_found_exception import (
    PoolManagerNotFoundException,
)
from src.exceptions.representative.representative_not_found_exception import (
    RepresentativeNotFoundException,
)
from src.exceptions.swimming_coach.swimming_coach_not_found_exception import (
    SwimmingCoachNotFoundException,
)
from src.models import get_db

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config import settings
from src.models.admin import Admin
from src.models.pool_manager import PoolManager
from src.models.representative import Representative
from src.models.swimming_coach import SwimmingCoach
from src.models.user import User

from src.routes.dto.auth.token_data import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORYTHM = settings.algorythm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return cast(str, pwd_context.hash(password))

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str | None) -> bool:
        return cast(bool, pwd_context.verify(plain_password, hashed_password))

    @staticmethod
    def generate_reset_token() -> tuple[str, str]:
        raw_token = secrets.token_urlsafe(32)
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
        return raw_token, hashed_token

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
            token_data = TokenData(
                user_id=user_id,
                representative_id=payload.get("representative_id"),
                admin_id=payload.get("admin_id"),
                pool_manager_id=payload.get("pool_manager_id"),
                swimming_coach_id=payload.get("swimming_coach_id"),
            )
        except JWTError:
            raise credential_exception
        return token_data

    @staticmethod
    def get_current_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credential",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data: TokenData = Security.verify_access_token(
            token, credential_exception
        )
        user = db.query(User).filter_by(id=token_data.user_id).first()
        return user

    @staticmethod
    def get_current_representative(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credential",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data: TokenData = Security.verify_access_token(
            token, credential_exception
        )
        representative = (
            db.query(Representative)
            .filter_by(id=token_data.representative_id)
            .one_or_none()
        )
        if not representative:
            raise RepresentativeNotFoundException("Representative not found")
        return representative

    @staticmethod
    def get_current_admin(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credential",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data: TokenData = Security.verify_access_token(
            token, credential_exception
        )
        admin = db.query(Admin).filter_by(id=token_data.admin_id).one_or_none()
        if not admin:
            raise AdminNotFoundException("Admin not found")
        return admin

    @staticmethod
    def get_current_pool_manager(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credential",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data: TokenData = Security.verify_access_token(
            token, credential_exception
        )
        pool_manager = (
            db.query(PoolManager).filter_by(id=token_data.pool_manager_id).one_or_none()
        )
        if not pool_manager:
            raise PoolManagerNotFoundException("Admin not found")
        return pool_manager

    @staticmethod
    def get_current_swimming_coach(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credential",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data: TokenData = Security.verify_access_token(
            token, credential_exception
        )
        swimming_coach = (
            db.query(SwimmingCoach)
            .filter_by(id=token_data.swimming_coach_id)
            .one_or_none()
        )
        if not swimming_coach:
            raise SwimmingCoachNotFoundException("Admin not found")
        return swimming_coach
