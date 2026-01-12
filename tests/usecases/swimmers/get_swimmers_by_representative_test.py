from src.usecases.swimmers.get_swimmers_by_representative import (
    get_swimmers_by_representative,
)
from tests.fixtures.swimmer_factory import SwimmerFactory


class TestGetSwimmersByRepresentative:
    def test_get_swimmers_by_representative(
        self, swimmer_repo, authenticated_representative
    ):
        swimmer_1 = SwimmerFactory(representatives=[authenticated_representative])
        swimmer_2 = SwimmerFactory(representatives=[authenticated_representative])
        unrelated_swimmer = SwimmerFactory()

        response = get_swimmers_by_representative(
            swimmer_repo, authenticated_representative
        )

        assert len(response) == 2
        assert response[0].first_name == swimmer_2.first_name
        assert response[0].last_name == swimmer_2.last_name
        assert response[0].birth_date == swimmer_2.birth_date
        assert response[1].first_name == swimmer_1.first_name
        assert response[1].last_name == swimmer_1.last_name
        assert response[1].birth_date == swimmer_1.birth_date
        assert unrelated_swimmer not in response
