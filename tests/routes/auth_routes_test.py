import uuid
from unittest.mock import patch

import pytest
from jose import jwt

from src.models.password_reset_token import PasswordResetToken
from src.routes.dto.auth.token import Token
from src.services.security import ALGORYTHM, SECRET_KEY, Security
from tests.fixtures.swimming_pool_factory import SwimmingPoolFactory
from tests.fixtures.user_factory import UserFactory


class TestLoginUser:
    def test_login_user(self, client, security, db_session):
        swimming_pool = SwimmingPoolFactory(pool_name="test pool")

        user = UserFactory(email="test@example.com")

        response = client.post(
            "/auth/login",
            data={"username": user.email, "password": "pass"},
            headers={"subdomain": swimming_pool.slug},
        )

        assert response.status_code == 200
        login_response = Token(**response.json())
        payload = jwt.decode(
            login_response.access_token, SECRET_KEY, algorithms=[ALGORYTHM]
        )
        user_id: str = payload.get("user_id")
        assert uuid.UUID(user_id) == user.id
        assert login_response.token_type == "bearer"

    @pytest.mark.parametrize(
        "email, password, status_code",
        [
            ("wrongemail@example.com", "pass", 403),
            ("usertest123@example.com", "wrong_password", 403),
            ("wrongemail@example.com", "wrong_password", 403),
        ],
    )
    def test_incorrect_login(self, client, email, password, status_code):
        swimming_pool = SwimmingPoolFactory(pool_name="test pool")
        response = client.post(
            "/auth/login",
            data={"username": email, "password": password},
            headers={"subdomain": swimming_pool.slug},
        )
        assert response.status_code == status_code
        assert response.json().get("detail") == "Invalid Credential"


@patch("src.usecases.auth.request_password_reset_usecase.EmailService.send_reset_email")
class TestRequestPasswordUser:
    def test_request_password_user(self, mock_send_email, client, security, db_session):
        user = UserFactory(email="test@example.com")
        response = client.post(
            "/auth/password-reset/request", json={"email": user.email}
        )
        assert response.status_code == 200
        mock_send_email.assert_called_once()


class TestPasswordReset:
    def test_password_reset_user(self, client, security, db_session):
        user = UserFactory(email="test@example.com")
        raw_token, token_hash = Security().generate_reset_token()
        token = PasswordResetToken(  # type: ignore[call-arg]
            user_id=user.id,
            token_hash=token_hash,
        )
        db_session.add(token)
        db_session.commit()

        response = client.post(
            "/auth/password-reset/confirm",
            json={"token": raw_token, "new_password": "newpassword"},
        )
        assert response.status_code == 200
