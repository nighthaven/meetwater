from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from src.models import db_dependency
from src.models.admin import Admin
from src.models.pool_manager import PoolManager
from src.models.representative import Representative
from src.models.swimming_coach import SwimmingCoach
from src.models.user import User
from src.routes.dto.auth.token import Token
from src.services.security import Security

router = APIRouter(tags=["Authentification"])


@router.post("/login", response_model=Token)
def login(
    db: db_dependency,
    credential: Annotated[OAuth2PasswordRequestForm, Depends()],
    security: Annotated[Any, Depends(Security)],
):
    user = db.query(User).filter(User.email == credential.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential"
        )
    if not security.verify_password(credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential"
        )
    user_id = str(user.id)
    representative = db.query(Representative).filter_by(user_id=user_id).one_or_none()
    admin = db.query(Admin).filter_by(user_id=user_id).one_or_none()
    pool_manager = db.query(PoolManager).filter_by(user_id=user_id).one_or_none()
    swimming_coach = db.query(SwimmingCoach).filter_by(user_id=user_id).one_or_none()

    access_token = security.create_access_token(
        data={
            "user_id": user_id,
            "representative_id": str(representative.id) if representative else None,
            "admin_id": str(admin.id) if admin else None,
            "pool_manager_id": str(pool_manager.id) if pool_manager else None,
            "swimming_coach_id": str(swimming_coach.id) if swimming_coach else None,
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}
