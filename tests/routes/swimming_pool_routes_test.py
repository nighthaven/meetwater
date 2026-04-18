from tests.fixtures.swimming_pool_factory import SwimmingPoolFactory


class TestSwimmingPoolRoutes:
    def test_create_swimming_pool_as_admin(self, admin_client, db_session):
        payload = {
            "pool_name": "Piscine Olympique",
            "address": "1 rue de la Piscine",
            "city": "Paris",
            "post_code": "75001",
        }
        response = admin_client.post("/swimming_pool/", json=payload)
        assert response.status_code == 201
        assert response.json()["pool_name"] == "Piscine Olympique"
        assert "id" in response.json()
        assert "slug" in response.json()

    def test_create_swimming_pool_requires_admin(self, client):
        payload = {
            "pool_name": "Piscine Olympique",
            "address": "1 rue de la Piscine",
            "city": "Paris",
            "post_code": "75001",
        }
        response = client.post("/swimming_pool/", json=payload)
        assert response.status_code == 401

    def test_get_swimming_pool(self, representative_client):
        swimming_pool = SwimmingPoolFactory()

        response = representative_client.get(
            "/swimming_pool/",
            headers={"subdomain": swimming_pool.slug},
        )
        assert response.status_code == 200
        assert response.json()["pool_name"] == swimming_pool.pool_name
        assert response.json()["slug"] == swimming_pool.slug
        assert response.json()["address"] == swimming_pool.address
        assert response.json()["city"] == swimming_pool.city
        assert response.json()["post_code"] == swimming_pool.post_code
