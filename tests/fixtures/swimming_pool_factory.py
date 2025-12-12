import factory

from src.models.swimming_pool import SwimmingPool


class SwimmingPoolFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = SwimmingPool
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    pool_name = factory.Sequence(lambda n: f"swimming_pool_from_city{n}")
    address = factory.Faker("address")
    city = factory.Faker("city")
    post_code = factory.Faker("postcode")
