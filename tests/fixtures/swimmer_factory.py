from src.models.link.swimmer_representative import SwimmerRepresentative
from src.models.swimmer import Swimmer
import factory


class SwimmerFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = Swimmer
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birth_date = factory.Faker("date_of_birth", minimum_age=5, maximum_age=17)

    @factory.post_generation
    def representatives(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for representative in extracted:
                SwimmerRepresentativeFactory(
                    swimmer=self, representative=representative
                )


class SwimmerRepresentativeFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = SwimmerRepresentative
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    representative = None
    swimmer = None
