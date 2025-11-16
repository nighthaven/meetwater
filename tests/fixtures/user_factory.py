import factory

from src.models.user import User
from src.services.security import Security


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = User
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: Security().hash_password("pass"))  # type: ignore[no-untyped-call]
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
