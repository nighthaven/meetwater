from unittest.mock import patch
from src.usecases.auth.request_password_reset_usecase import (
    request_password_reset_usecase,
)
from tests.fixtures.user_factory import UserFactory


class TestRequestPasswordResetUsecase:

    @patch(
        "src.usecases.auth.request_password_reset_usecase.EmailService.send_reset_email"
    )
    def test_request_password_reset(self, mock_send_email, auth_repo):
        user = UserFactory()

        response = request_password_reset_usecase(
            email=user.email,
            auth_repository=auth_repo,
        )

        mock_send_email.assert_called_once()
        assert response["message"] == "Si un compte existe, un email a été envoyé"
