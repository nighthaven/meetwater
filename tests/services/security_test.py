from fastapi import status, HTTPException


class SecurityTests:
    def __init__(self, security):
        self.security = security

    def test_hash_password(self):
        pwd = "mysecret"
        hashed = self.security.hash_password(pwd)
        assert hashed != pwd
        assert self.security.verify_password(pwd, hashed)
        assert not self.security.verify_password("wrong", hashed)

    def test_create_and_verify_access_token(self, test_user):
        token = self.security.create_access_token({"user_id": str(test_user.id)})
        assert token is not None
        cred_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credential",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data = self.security.verify_access_token(token, cred_exception)
        assert str(test_user.id) == str(token_data.id)

    def test_get_current_user(self, client, test_user):
        token = self.security.create_access_token({"user_id": str(test_user.id)})
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
