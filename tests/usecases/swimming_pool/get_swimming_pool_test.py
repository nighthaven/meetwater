import pytest

from src.exceptions.swimming_pool.swimming_pool_not_found_exception import (
    SwimmingPoolNotFoundException,
)
from src.models.enums.coach_activity import CoachActivity
from src.usecases.swimming_pool.get_swimming_pool import get_swimming_pool_from_slug
from tests.fixtures.coach_schedule_factory import CoachScheduleFactory
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory
from tests.fixtures.swimming_pool_factory import SwimmingPoolFactory


class TestGetSwimmingPool:
    def test_get_swimming_pool(self, swimming_pool_repo, mock_request_with_subdomain):
        swimming_pool = SwimmingPoolFactory()
        swimming_coach = SwimmingCoachFactory(swimming_pool_id=swimming_pool.id)
        CoachScheduleFactory(swimming_coach=swimming_coach)
        mock_request = mock_request_with_subdomain(swimming_pool.slug)

        response = get_swimming_pool_from_slug(mock_request, swimming_pool_repo)

        assert response["pool_name"] == swimming_pool.pool_name
        assert response["slug"] == swimming_pool.slug
        assert response["address"] == swimming_pool.address
        assert response["city"] == swimming_pool.city
        assert response["post_code"] == swimming_pool.post_code
        assert response["schedules"] == swimming_pool.schedules
        assert (
            response["coaches_schedules"][0].activity
            == CoachActivity.CHILD_INTERMEDIATE
        )
        assert (
            response["coaches_schedules"][0].scheduled_at
            == swimming_coach.schedules[0].scheduled_at
        )

    def test_get_swimming_pool_not_found(
        self, swimming_pool_repo, mock_request_with_subdomain
    ):
        mock_request = mock_request_with_subdomain("something_wrong")

        with pytest.raises(SwimmingPoolNotFoundException):
            get_swimming_pool_from_slug(mock_request, swimming_pool_repo)
