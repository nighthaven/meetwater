import factory
import random
from datetime import timedelta, date

from src.models.swimming_coach import SwimmingCoach
from src.services.security import Security


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

    # information nécessaire pour la génération du user
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: Security().hash_password("pass"))


def random_date_within_years(years: int) -> date:
    today = date.today()
    start_date = today - timedelta(days=365 * years)
    random_days = random.randint(0, (today - start_date).days)
    return start_date + timedelta(days=random_days)
