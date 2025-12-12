from tests.fixtures.swimming_pool_factory import SwimmingPoolFactory


class TestPoolManagerRoutes:
    def test_pool_manager_routes(self, pool_manager_repo, admin_client):
        swimming_pool = SwimmingPoolFactory()
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "swimming_pool_id": str(swimming_pool.id),
            "email": "johndoe@example.com",
            "raw_password": "password",
        }
        response = admin_client.post("/pool_managers", json=payload)

        assert response.status_code == 201

        query_pool_manager = pool_manager_repo.get()
        assert query_pool_manager[0].first_name == payload["first_name"]
        assert query_pool_manager[0].last_name == payload["last_name"]
        assert query_pool_manager[0].user.email == payload["email"]
