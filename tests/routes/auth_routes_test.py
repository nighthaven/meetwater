import uuid

import pytest
from jose import jwt
from src.routes.dto.auth.token import Token
from src.services.security import ALGORYTHM, SECRET_KEY
from tests.fixtures.user_factory import UserFactory


class TestLoginUser:
    def test_login_user(self, client, security, db_session):

        user = UserFactory(email="test@example.com")

        response = client.post(
            "/login", data={"username": user.email, "password": "pass"}
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
        response = client.post("/login", data={"username": email, "password": password})
        assert response.status_code == status_code
        assert response.json().get("detail") == "Invalid Credential"
