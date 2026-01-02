from tests.fixtures.swimming_pool_factory import SwimmingPoolFactory


class TestSwimmingPoolRoutes:
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
