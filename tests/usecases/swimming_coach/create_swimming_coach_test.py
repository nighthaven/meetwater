from datetime import datetime, timezone, timedelta

from src.models.swimming_coach import SwimmingCoach
from src.routes.dto.swimming_coach.swimming_coach_query import SwimmingCoachQuery
from src.usecases.swimming_coach.create_swimming_coach import (
    create_swimming_coach_usecase,
)


class TestCreateSwimmingCoach:
    def test_create_swimming_coach(
        self, security, swimming_coach_repo, authenticated_pool_manager, db_session
    ):
        caep_date = (datetime.now(timezone.utc) - timedelta(days=2 * 365)).date()
        pse_date = (datetime.now(timezone.utc) - timedelta(days=200)).date()
        query = SwimmingCoachQuery(
            first_name="John",
            last_name="Smith",
            last_caep_certification_date=caep_date,
            last_pse_certification_date=pse_date,
            email="johnsmith@example.com",
            raw_password="password",
        )

        create_swimming_coach_usecase(
            query, security, swimming_coach_repo, authenticated_pool_manager
        )

        query_swimming_coach = db_session.query(SwimmingCoach).all()
        assert len(query_swimming_coach) == 1
        assert query_swimming_coach[0].first_name == query.first_name
        assert query_swimming_coach[0].last_name == query.last_name
        assert query_swimming_coach[0].last_caep_certification_date == caep_date
        assert query_swimming_coach[0].last_pse_certification_date == pse_date
        assert query_swimming_coach[0].user.email == query.email
