from datetime import date, datetime, timedelta, timezone

from src.models.enums.swimmer_level import SwimmerLevel
from tests.fixtures.booking_factory import BookingFactory
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


class TestCreateBooking:
    def test_create_booking(self, client):
        user = UserFactory()
        swimmer_1 = SwimmerFactory(link_user=user)
        SwimmerFactory(link_user=user)
        datetime_booked_at = datetime.now(timezone.utc) + timedelta(days=2)

        payload = {
            "booked_at": str(datetime_booked_at),
            "swimmers_ids": [str(swimmer_1.id)],
        }
        response = client.post(
            f"/users/{user.id}/bookings",
            json=payload,
        )

        assert response.status_code == 201


class TestGetBooking:
    def test_get_booking(self, client):
        user = UserFactory()
        swimmer = SwimmerFactory(link_user=user)
        booking_1 = BookingFactory(swimmers=swimmer)

        response = client.get(
            f"/users/{user.id}/bookings",
        )

        assert response.status_code == 200
        assert response.json()["user_first_name"] == user.first_name
        assert response.json()["user_last_name"] == user.last_name
        assert response.json()["user_email"] == user.email
        assert (
            response.json()["bookings"][0]["booked_at"]
            == booking_1.booked_at.isoformat()
        )
        assert (
            response.json()["bookings"][0]["created_at"]
            == booking_1.created_at.isoformat()
        )
        assert response.json()["bookings"][0]["time_slot"] == booking_1.time_slot
        assert response.json()["bookings"][0]["status"] == booking_1.status
        assert (
            response.json()["bookings"][0]["swimmers"][0]["first_name"]
            == swimmer.first_name
        )
        assert (
            response.json()["bookings"][0]["swimmers"][0]["last_name"]
            == swimmer.last_name
        )
        assert (
            response.json()["bookings"][0]["swimmers"][0]["birth_date"]
            == swimmer.birth_date.isoformat()
        )
        assert (
            response.json()["bookings"][0]["swimmers"][0]["level"]
            == swimmer.level.value
        )
