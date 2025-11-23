from uuid import UUID

import pytest

from src.exceptions.user.user_not_found_exception import UserNotFoundException
from src.usecases.get_bookings import get_bookings_by_user_id
from tests.fixtures.booking_factory import BookingFactory
from tests.fixtures.swimmer_factory import SwimmerFactory
from tests.fixtures.user_factory import UserFactory


class TestGetBookingsByUserId:
    def test_get_bookings_by_user_id(self, user_repo):
        user = UserFactory()
        swimmer = SwimmerFactory(link_user=user)
        booking_1 = BookingFactory(swimmers=swimmer)
        BookingFactory(swimmers=swimmer)

        response = get_bookings_by_user_id(user.id, user_repo)

        assert len(response) == 2
        assert response["user"]["id"] == user.id
        assert response["user"]["first_name"] == user.first_name
        assert response["user"]["last_name"] == user.last_name
        assert response["user"]["email"] == user.email
        for booking in response["bookings"]:
            booking["swimmers"][0]["id"] == swimmer.id
            booking["swimmers"][0]["first_name"] == swimmer.first_name
            booking["swimmers"][0]["last_name"] == swimmer.last_name
            booking["swimmers"][0]["birth_date"] == swimmer.birth_date
            booking["swimmers"][0]["level"] == swimmer.level
            booking["booked_at"] == booking_1.booked_at
            booking["created_at"] == booking_1.created_at
            booking["time_slot"] == booking_1.time_slot

    def test_get_bookings_by_user_id_user_not_found(self, user_repo):
        swimmer = SwimmerFactory()
        BookingFactory(swimmers=swimmer)
        BookingFactory(swimmers=swimmer)

        with pytest.raises(UserNotFoundException):
            get_bookings_by_user_id(
                UUID("a97afb97-8bdb-4d58-9889-7ef96401643a"), user_repo
            )
