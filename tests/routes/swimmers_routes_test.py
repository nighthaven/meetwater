from src.models.enums.swimmer_level import SwimmerLevel
from datetime import datetime, timedelta

from src.models.swimmer import Swimmer
from tests.fixtures.swimmer_factory import SwimmerFactory


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

    def test_get_swimmers(self, representative_client, db_session):
        representative = representative_client.user_type
        swimmer_1 = SwimmerFactory(representatives=[representative])
        swimmer_2 = SwimmerFactory(representatives=[representative])

        response = representative_client.get("/swimmers")
        assert response.status_code == 200
        assert len(response.json()["swimmers"]) == 2
        assert response.json()["swimmers"][0]["first_name"] == swimmer_1.first_name
        assert response.json()["swimmers"][0]["last_name"] == swimmer_1.last_name
        assert (
            response.json()["swimmers"][0]["birth_date"]
            == swimmer_1.birth_date.isoformat()
        )
        assert response.json()["swimmers"][0]["level"] == swimmer_1.level.value
        assert response.json()["swimmers"][1]["first_name"] == swimmer_2.first_name
        assert response.json()["swimmers"][1]["last_name"] == swimmer_2.last_name
        assert (
            response.json()["swimmers"][1]["birth_date"]
            == swimmer_2.birth_date.isoformat()
        )
        assert response.json()["swimmers"][1]["level"] == swimmer_2.level.value
