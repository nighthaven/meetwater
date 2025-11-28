import factory

from src.models.representative import Representative
from src.services.security import Security


class RepresentativeFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = Representative
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=90)

    # information nécessaire pour la génération du user
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: Security().hash_password("pass"))
