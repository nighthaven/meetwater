from typing import Annotated
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from src.exceptions.auth.invalid_credential_exception import InvalidCredentialException
from src.repositories.admin_repository import AdminRepository
from src.repositories.auth_repository import AuthRepository
from src.repositories.pool_manager_repository import PoolManagerRepository
from src.repositories.representative_repository import RepresentativeRepository
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.services.security import Security


def login_usecase(
    credential: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_repository: AuthRepository,
    representative_repository: RepresentativeRepository,
    pool_manager_repository: PoolManagerRepository,
    swimming_coach_repository: SwimmingCoachRepository,
    admin_repository: AdminRepository,
):
    security = Security()
    user = auth_repository.find(credential.username)
    if not user or not security.verify_password(credential.password, user.password):
        raise InvalidCredentialException("Invalid Credential")
    user_id = user.id
    representative = representative_repository.find_by_user_id(user_id)
    admin = admin_repository.find_by_user_id(user_id)
    pool_manager = pool_manager_repository.find_by_user_id(user_id)
    swimming_coach = swimming_coach_repository.find_by_user_id(user_id)

    access_token = security.create_access_token(
        data={
            "user_id": str(user_id),
            "representative_id": str(representative.id) if representative else None,
            "admin_id": str(admin.id) if admin else None,
            "pool_manager_id": str(pool_manager.id) if pool_manager else None,
            "swimming_coach_id": str(swimming_coach.id) if swimming_coach else None,
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}
