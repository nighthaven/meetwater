from datetime import date

from src.models.enums.swimmer_level import SwimmerLevel
from tests.fixtures.swimmer_factory import SwimmerFactory
from tests.fixtures.user_factory import UserFactory


class TestCreateUser:
    def test_create_users(self, client):
        response = client.post(
            "/users/",
            json={
                "email": "hello123@gmail.com",
                "password": "pass",
                "first_name": "Tom",
                "last_name": "Bombadil",
                "birth_date": date(2000, 1, 16).isoformat(),
            },
        )
        assert response.status_code == 201


class TestCreateSwimmer:
    def test_create_swimmers(self, client):
        user = UserFactory()
        payload = {
            "first_name": "frodo",
            "last_name": "Saquet",
            "birth_date": date(2000, 1, 16).isoformat(),
            "level": SwimmerLevel.INTERMEDIATE.value,
        }
        response = client.post(
            f"/users/{user.id}/swimmer",
            json=payload,
        )
        assert response.status_code == 201


class TestGetUser:
    def test_get_user_by_id(self, client):
        user = UserFactory()
        swimmer = SwimmerFactory(link_user=user)
        response = client.get(
            "/users/{}".format(user.id),
        )
        assert response.status_code == 200
        assert response.json()["first_name"] == user.first_name
        assert response.json()["last_name"] == user.last_name
        assert response.json()["email"] == user.email
        assert response.json()["swimmers"][0]["first_name"] == swimmer.first_name
        assert response.json()["swimmers"][0]["last_name"] == swimmer.last_name
        assert response.json()["swimmers"][0]["birth_date"] == str(swimmer.birth_date)
        assert response.json()["swimmers"][0]["level"] == swimmer.level.value
