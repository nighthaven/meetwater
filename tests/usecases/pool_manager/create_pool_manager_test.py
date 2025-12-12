from src.routes.dto.pool_manager.pool_manager_query import PoolManagerQuery
from src.usecases.pool_manager.create_pool_manager import create_pool_manager_usecase
from tests.fixtures.swimming_pool_factory import SwimmingPoolFactory


class TestCreatePoolManager:
    def test_create_pool_manager(
        self, security, swimming_pool_repo, pool_manager_repo, admin_client
    ):
        swimming_pool = SwimmingPoolFactory()
        query = PoolManagerQuery(
            first_name="John",
            last_name="Doe",
            swimming_pool_id=swimming_pool.id,
            email="johndoe@example.com",
            raw_password="password",
        )

        create_pool_manager_usecase(
            query, security, swimming_pool_repo, pool_manager_repo, admin_client
        )

        query_pool_manager = pool_manager_repo.get()
        assert len(query_pool_manager) == 1
        assert query_pool_manager[0].first_name == query.first_name
        assert query_pool_manager[0].last_name == query.last_name
        assert query_pool_manager[0].user.email == query.email
