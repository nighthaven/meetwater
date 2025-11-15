import factory

from src.models.enums.user_level import UserLevel
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
    birth_date = factory.Faker("date_of_birth", minimum_age=5, maximum_age=18)
    representative = "Simone"
    level = UserLevel.INTERMEDIATE
    created_at = factory.Faker("date_time")
