from tests.fixtures.user_factory import UserFactory
from src.services.security import Security


class TestAdminRoutes:
    def test_bootstrap_creates_first_admin(self, client, admin_repo):
        payload = {
            "first_name": "Tom",
            "last_name": "Valoteau",
            "email": "tom@meetwater.fr",
            "raw_password": "password123!",
        }

        response = client.post("/admin/bootstrap", json=payload)

        assert response.status_code == 201
        assert admin_repo.count() == 1

    def test_bootstrap_fails_if_admin_already_exists(self, client, admin_repo):
        payload = {
            "first_name": "Tom",
            "last_name": "Valoteau",
            "email": "tom@meetwater.fr",
            "raw_password": "password123!",
        }
        client.post("/admin/bootstrap", json=payload)

        response = client.post("/admin/bootstrap", json=payload)

        assert response.status_code == 409

    def test_create_admin_requires_auth(self, client):
        payload = {
            "first_name": "Boris",
            "last_name": "Le Bon",
            "email": "boris@meetwater.fr",
            "raw_password": "password123!",
        }

        response = client.post("/admin/", json=payload)

        assert response.status_code == 401

    def test_create_admin_as_admin(self, admin_client, admin_repo):
        payload = {
            "first_name": "Boris",
            "last_name": "Le Bon",
            "email": "boris@meetwater.fr",
            "raw_password": "password123!",
        }

        response = admin_client.post("/admin/", json=payload)

        assert response.status_code == 201
        assert admin_repo.count() == 2


class TestAdminResetUserPassword:
    def test_reset_user_password_as_admin(self, admin_client, auth_repo, db_session):
        user = UserFactory(email="target@example.com")
        db_session.commit()

        response = admin_client.post(
            "/admin/reset-user-password",
            json={"email": "target@example.com", "new_password": "NewPass123!"},
        )

        assert response.status_code == 204
        db_session.refresh(user)
        assert Security().verify_password("NewPass123!", user.password)

    def test_reset_user_password_unknown_email(self, admin_client):
        response = admin_client.post(
            "/admin/reset-user-password",
            json={"email": "nobody@example.com", "new_password": "NewPass123!"},
        )
        assert response.status_code == 404

    def test_reset_user_password_requires_admin(self, client):
        response = client.post(
            "/admin/reset-user-password",
            json={"email": "target@example.com", "new_password": "NewPass123!"},
        )
        assert response.status_code == 401
