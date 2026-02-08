import factory

from src.models.coach_pack import CoachPack
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory


class CoachPackFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore[misc]
    class Meta:
        model = CoachPack
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    swimming_coach = factory.SubFactory(SwimmingCoachFactory)
    sessions_count = 1
    price = 20
    final_price = 20
