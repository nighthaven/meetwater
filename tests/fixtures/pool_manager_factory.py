import factory

from src.models.pool_manager import PoolManager
from src.services.security import Security


class PoolManagerFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = PoolManager
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    # information nécessaire pour la génération du user
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: Security().hash_password("pass"))
