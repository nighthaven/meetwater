import pytest
from datetime import datetime, timedelta, timezone
from uuid import UUID

from src.exceptions.booking.booking_cancellation_minimum_exception import (
    BookingCancellationMinimumException,
)
from src.exceptions.booking.booking_not_found_exception import BookingNotFoundException
from src.usecases.booking.delete_booking_usecase import delete_booking_usecase
from tests.fixtures.booking_factory import BookingFactory


class TestDeleteBookingByCoach:
    def test_delete_booking(self, booking_repo, authenticated_swimming_coach):
        booking = BookingFactory(
            appointment_at=datetime.now(timezone.utc) + timedelta(hours=2)
        )
        user = authenticated_swimming_coach.user

        delete_booking_usecase(booking.id, booking_repo, user)

        booking_query = booking_repo.get_all()
        assert len(booking_query) == 0


class TestDeleteBookingByRepresentative:
    def test_delete_booking(self, booking_repo, authenticated_representative):
        booking = BookingFactory(
            appointment_at=datetime.now(timezone.utc) + timedelta(days=2)
        )
        user = authenticated_representative.user

        delete_booking_usecase(booking.id, booking_repo, user)

        booking_query = booking_repo.get_all()
        assert len(booking_query) == 0

    def test_delete_booking_not_found(self, booking_repo, authenticated_representative):
        user = authenticated_representative.user

        with pytest.raises(BookingNotFoundException):
            delete_booking_usecase(
                UUID("b90ad427-4d84-401b-bed9-f4ee18949f4f"), booking_repo, user
            )

    def test_delete_booking_less_one_day(
        self, booking_repo, authenticated_representative
    ):
        booking = BookingFactory(
            appointment_at=datetime.now(timezone.utc) + timedelta(hours=7)
        )
        user = authenticated_representative.user

        with pytest.raises(BookingCancellationMinimumException):
            delete_booking_usecase(booking.id, booking_repo, user)
