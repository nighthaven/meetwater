import factory
import random
from datetime import timedelta, date

from src.models.link.swimmers_coachs import SwimmerCoach
from src.models.swimming_coach import SwimmingCoach
from src.services.security import Security
from tests.fixtures.swimming_pool_factory import SwimmingPoolFactory


def random_date_within_years(years: int) -> date:
    today = date.today()
    start_date = today - timedelta(days=365 * years)
    random_days = random.randint(0, (today - start_date).days)
    return start_date + timedelta(days=random_days)


class SwimmingCoachFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = SwimmingCoach
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    last_caep_certification_date = factory.LazyFunction(
        lambda: random_date_within_years(5)
    )

    last_pse_certification_date = factory.LazyFunction(
        lambda: random_date_within_years(1)
    )
    swimming_pool_id = factory.LazyFunction(lambda: SwimmingPoolFactory().id)

    # information nécessaire pour la génération du user
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: Security().hash_password("pass"))

    @factory.post_generation
    def schedules(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for schedule in extracted:
                schedule.swimming_coach = self

    @factory.post_generation
    def swimmers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for swimmer in extracted:
                SwimmerCoachFactory(swimmer=swimmer, swimming_coach=self)


class SwimmerCoachFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = SwimmerCoach
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    swimmer = None
    swimming_coach = None
