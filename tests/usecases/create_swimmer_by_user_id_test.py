from src.models.enums.swimmer_level import SwimmerLevel
from src.routes.dto.swimmer.swimmer_query import SwimmerQuery
from src.usecases.create_swimmer import create_swimmer_by_user_id
from tests.fixtures.user_factory import UserFactory
from datetime import date


class TestCreateSwimmerByUser:
    def test_create_swimmer_by_user_id(self, user_repo):
        user = UserFactory()
        birth_date = date.today().replace(year=date.today().year - 18)
        payload = SwimmerQuery(
            first_name="Frodo",
            last_name="Saquet",
            birth_date=birth_date,
            level=SwimmerLevel.BEGINNER,
        )

        create_swimmer_by_user_id(
            user_id=user.id, query=payload, user_repository=user_repo
        )

        swimmers = user_repo.get_swimmer_by_user_id(user.id)

        assert swimmers[0].first_name == "Frodo"
        assert swimmers[0].last_name == "Saquet"
        assert swimmers[0].birth_date == birth_date
        assert swimmers[0].level == SwimmerLevel.BEGINNER
