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
