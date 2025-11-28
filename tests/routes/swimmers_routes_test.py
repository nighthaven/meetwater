from src.models.enums.swimmer_level import SwimmerLevel
from datetime import datetime, timedelta

from src.models.swimmer import Swimmer


class TestSwimmersRoutes:
    def test_create_swimmer(self, representative_client, db_session):
        birth_date = datetime.now().date() - timedelta(days=6 * 365)
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": birth_date.isoformat(),
            "level": SwimmerLevel.BEGINNER.value,
        }
        response = representative_client.post("/swimmers", json=payload)

        assert response.status_code == 201
        query_swimmers = db_session.query(Swimmer).all()
        assert len(query_swimmers) == 1
        assert query_swimmers[0].first_name == "John"
        assert query_swimmers[0].last_name == "Doe"
        assert query_swimmers[0].birth_date == birth_date
        assert query_swimmers[0].level == SwimmerLevel.BEGINNER
