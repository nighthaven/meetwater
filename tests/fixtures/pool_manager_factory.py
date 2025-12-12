import factory

from src.models.pool_manager import PoolManager
from src.services.security import Security
from tests.fixtures.swimming_pool_factory import SwimmingPoolFactory


class PoolManagerFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = PoolManager
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    swimming_pool_id = factory.LazyFunction(lambda: SwimmingPoolFactory().id)

    # information nécessaire pour la génération du user
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: Security().hash_password("pass"))
