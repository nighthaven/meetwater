from src.models.password_reset_token import PasswordResetToken
from src.services.security import Security
from src.usecases.auth.reset_password_usecase import reset_password_usecase
from tests.fixtures.user_factory import UserFactory


class TestResetPassword:
    def test_reset_password(self, auth_repo):
        user = UserFactory()
        raw_token, token_hash = Security().generate_reset_token()
        reset_token = PasswordResetToken(  # type: ignore[call-arg]
            user_id=user.id,
            token_hash=token_hash,
        )

        auth_repo.db.add(reset_token)
        auth_repo.db.commit()

        reset_password_usecase(raw_token, "newpassword", auth_repo)

        auth_repo.db.refresh(user)
        assert Security().verify_password("newpassword", user.password)
