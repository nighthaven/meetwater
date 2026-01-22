from uuid import UUID
import pytest

from src.exceptions.swimming_coach.swimming_coach_not_current_coach import (
    SwimmingCoachNotCurrentCoach,
)
from src.exceptions.swimming_coach.swimming_coach_not_found_exception import (
    SwimmingCoachNotFoundException,
)
from src.usecases.swimming_coach.get_swimming_coach_by_id import (
    get_swimming_coach_by_id,
)
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory


class TestGetSwimmingCoach:
    def test_get_swimming_coach(
        self, swimming_coach_repo, authenticated_swimming_coach
    ):
        swimming_coach = SwimmingCoachFactory()

        response = get_swimming_coach_by_id(
            swimming_coach.id, swimming_coach_repo, swimming_coach
        )

        assert response.id == swimming_coach.id
        assert response.first_name == swimming_coach.first_name
        assert response.last_name == swimming_coach.last_name

    def test_get_swimming_coach_not_found(
        self, swimming_coach_repo, authenticated_swimming_coach
    ):
        swimming_coach = SwimmingCoachFactory()

        with pytest.raises(SwimmingCoachNotFoundException):
            get_swimming_coach_by_id(
                UUID("ef803846-4afe-427c-a16c-227d3104485b"),
                swimming_coach_repo,
                swimming_coach,
            )

    def test_get_swimming_coach_user_not_same_coach(
        self, swimming_coach_repo, authenticated_swimming_coach
    ):
        swimming_coach = SwimmingCoachFactory()
        current_coach = SwimmingCoachFactory()

        with pytest.raises(SwimmingCoachNotCurrentCoach):
            get_swimming_coach_by_id(
                swimming_coach.id, swimming_coach_repo, current_coach
            )
