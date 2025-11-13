from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.services.security import Security
from src.models.user import User
from src.models import db_dependency
from typing import Annotated, Any
from src.routes.dto.auth.token import Token


router = APIRouter(
    tags=["Authentification"]
)


@router.post("/login", response_model=Token)
def login(
        db: db_dependency,
        credential: Annotated[OAuth2PasswordRequestForm, Depends()],
        security: Annotated[Any, Depends(Security)],
):
    user = db.query(User).filter(User.email == credential.username).first()
    user_id = str(user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credential")
    if not security.verify_password(credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credential")

    access_token = security.create_access_token(data={"user_id": user_id})
    return {"access_token": access_token, "token_type": "bearer"}