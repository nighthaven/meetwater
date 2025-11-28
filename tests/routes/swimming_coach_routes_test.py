from datetime import datetime, timezone, timedelta

from src.models.swimming_coach import SwimmingCoach


class TestSwimmingCoachRoutes:
    def test_swimming_coach_routes(self, pool_manager_client, db_session):
        caep_date = (datetime.now(timezone.utc) - timedelta(days=2 * 365)).date()
        pse_date = (datetime.now(timezone.utc) - timedelta(days=200)).date()
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "last_caep_certification_date": caep_date.isoformat(),
            "last_pse_certification_date": pse_date.isoformat(),
            "email": "johndoe@example.com",
            "raw_password": "password",
        }
        response = pool_manager_client.post("/swimming_coaches", json=payload)
        assert response.status_code == 201
        query_swimming_coach = db_session.query(SwimmingCoach).all()
        assert len(query_swimming_coach) == 1
        assert query_swimming_coach[0].first_name == "John"
        assert query_swimming_coach[0].last_name == "Doe"
        assert query_swimming_coach[0].last_caep_certification_date == caep_date
        assert query_swimming_coach[0].last_pse_certification_date == pse_date
        assert query_swimming_coach[0].user.email == "johndoe@example.com"
