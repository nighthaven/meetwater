from datetime import datetime, timedelta

from src.models.enums.swimmer_level import SwimmerLevel
from src.routes.dto.swimmer.swimmer_query import SwimmerQuery
from src.usecases.swimmers.create_swimmer import create_swimmer_usecase
from tests.fixtures.representative_factory import RepresentativeFactory
from tests.fixtures.swimmer_factory import SwimmerFactory


class TestCreateSwimmer:
    def test_create_swimmer(
        self, representative_repo, swimmer_repo, authenticated_representative
    ):
        birth_date = datetime.now().date() - timedelta(days=6 * 365)
        query = SwimmerQuery(
            first_name="John",
            last_name="Smith",
            birth_date=birth_date,
            level=SwimmerLevel.BEGINNER,
        )
        create_swimmer_usecase(
            query, representative_repo, swimmer_repo, authenticated_representative
        )

        swimmer_query = swimmer_repo.get()
        assert swimmer_query[0].first_name == "John"
        assert swimmer_query[0].last_name == "Smith"
        assert swimmer_query[0].birth_date == birth_date
        assert swimmer_query[0].level == SwimmerLevel.BEGINNER

    def test_create_swimmer_already_exist(
        self, representative_repo, swimmer_repo, authenticated_representative
    ):
        another_representative = RepresentativeFactory()
        birth_date = datetime.now().date() - timedelta(days=6 * 365)
        swimmer = SwimmerFactory(
            first_name="John",
            last_name="Smith",
            birth_date=birth_date,
            representatives=[another_representative],
        )
        query = SwimmerQuery(
            first_name="John",
            last_name="Smith",
            birth_date=birth_date,
            level=SwimmerLevel.BEGINNER,
        )
        create_swimmer_usecase(
            query, representative_repo, swimmer_repo, authenticated_representative
        )

        assert len(swimmer.representatives) == 2
        assert (
            swimmer.representatives[0].representative.full_name
            == another_representative.full_name
        )
        assert (
            swimmer.representatives[1].representative.full_name
            == authenticated_representative.full_name
        )
