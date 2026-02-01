from typing import Annotated, Any
from pydantic import EmailStr

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from src.exceptions.auth.invalid_credential_exception import InvalidCredentialException
from src.repositories.admin_repository import AdminRepository
from src.repositories.auth_repository import AuthRepository
from src.repositories.pool_manager_repository import PoolManagerRepository
from src.repositories.representative_repository import RepresentativeRepository
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.routes.dto.auth.token import Token
from src.usecases.auth.login_usecase import login_usecase
from src.usecases.auth.request_password_reset_usecase import (
    request_password_reset_usecase,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    credential: Annotated[OAuth2PasswordRequestForm, Depends()],
    representative_repository: Annotated[Any, Depends(RepresentativeRepository)],
    pool_manager_repository: Annotated[Any, Depends(PoolManagerRepository)],
    swimming_coach_repository: Annotated[Any, Depends(SwimmingCoachRepository)],
    admin_repository: Annotated[Any, Depends(AdminRepository)],
    auth_repository=Depends(AuthRepository),
):
    try:
        return login_usecase(
            credential,
            auth_repository,
            representative_repository,
            pool_manager_repository,
            swimming_coach_repository,
            admin_repository,
        )
    except InvalidCredentialException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential"
        )


@router.post("/password-reset/request")
def request_password_reset(
    email: EmailStr,
    auth_repository: Annotated[Any, Depends(AuthRepository)],
):
    return request_password_reset_usecase(email, auth_repository)
