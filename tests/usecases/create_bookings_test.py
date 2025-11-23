import pytest
from uuid import UUID

from src.exceptions.booking.booking_already_taken_for_swimmer_exception import (
    BookingAlreadyTakenForSwimmerException,
)
from src.exceptions.booking.booking_must_be_in_the_futur_exception import (
    BookingMustBeInTheFutureException,
)
from src.exceptions.swimmer.swimmer_not_found_exception import SwimmerNotFoundException
from src.exceptions.user.user_not_found_exception import UserNotFoundException
from src.exceptions.user.user_not_linked_to_swimmer_exception import (
    UserNotLinkedToSwimmerException,
)
from src.models.enums.booking_status import BookingStatus
from src.routes.dto.booking.booking_query import BookingQuery
from src.usecases.create_bookings import create_bookings_usecase
from tests.fixtures.booking_factory import BookingFactory
from tests.fixtures.swimmer_factory import SwimmerFactory
from tests.fixtures.user_factory import UserFactory
from datetime import datetime, timedelta, timezone


class TestCreateBookings:
    def test_create_bookings_success(self, user_repo, swimmer_repo, booking_repo):
        user = UserFactory()
        swimmer = SwimmerFactory(link_user=user)

        datebooked = datetime.now(timezone.utc) + timedelta(days=2)
        payload = BookingQuery(
            booked_at=datebooked,
            swimmers_ids=[swimmer.id],
        )

        create_bookings_usecase(user.id, payload, user_repo, swimmer_repo, booking_repo)

        query_bookings = booking_repo.get_all()

        assert len(query_bookings) == 1
        assert query_bookings[0].booked_at.replace(microsecond=0) == datebooked.replace(
            microsecond=0
        )
        assert len(query_bookings[0].swimmers) == 1
        assert query_bookings[0].swimmers[0].swimmer.id == swimmer.id
        assert query_bookings[0].swimmers[0].swimmer.first_name == swimmer.first_name
        assert query_bookings[0].swimmers[0].swimmer.last_name == swimmer.last_name
        assert query_bookings[0].swimmers[0].swimmer.level == swimmer.level
        assert query_bookings[0].swimmers[0].swimmer.birth_date == swimmer.birth_date
        assert query_bookings[0].status == BookingStatus.ACCEPTED

    def test_create_booking_user_not_found(self, user_repo, swimmer_repo, booking_repo):
        user = UserFactory()
        swimmer = SwimmerFactory(link_user=user)

        datebooked = datetime.now() + timedelta(days=2)
        payload = BookingQuery(
            booked_at=datebooked,
            swimmers_ids=[swimmer.id],
        )

        with pytest.raises(UserNotFoundException):
            create_bookings_usecase(
                UUID("a54b8874-0625-4d4c-8c2a-163b94c08e1c"),
                payload,
                user_repo,
                swimmer_repo,
                booking_repo,
            )

    @pytest.mark.parametrize(
        "create_swimmer",
        [
            True,
            False,
        ],
    )
    def test_create_booking_swimmer_not_found(
        self, user_repo, swimmer_repo, booking_repo, create_swimmer
    ):
        user = UserFactory()
        if create_swimmer:
            SwimmerFactory(link_user=user)

        datebooked = datetime.now() + timedelta(days=2)
        payload = BookingQuery(
            booked_at=datebooked,
            swimmers_ids=(
                [] if create_swimmer else [UUID("27dbb4e3-5ef6-4777-8811-daa9927e8923")]
            ),
        )

        with pytest.raises(SwimmerNotFoundException):
            create_bookings_usecase(
                user.id, payload, user_repo, swimmer_repo, booking_repo
            )

    def test_create_booking_swimmer_not_linked_to_user(
        self, user_repo, swimmer_repo, booking_repo
    ):
        user = UserFactory()
        SwimmerFactory(link_user=user)
        swimmer_not_linked = SwimmerFactory()

        datebooked = datetime.now() + timedelta(days=2)
        payload = BookingQuery(
            booked_at=datebooked,
            swimmers_ids=[swimmer_not_linked.id],
        )

        with pytest.raises(UserNotLinkedToSwimmerException):
            create_bookings_usecase(
                user.id, payload, user_repo, swimmer_repo, booking_repo
            )

    @pytest.mark.parametrize(
        "offset_minutes",
        [
            0,
            10,
        ],
    )
    def test_create_booking_already_booked_for_swimmer(
        self, user_repo, swimmer_repo, booking_repo, offset_minutes
    ):
        user = UserFactory()
        swimmer = SwimmerFactory(link_user=user)
        base_start = datetime.now(timezone.utc) + timedelta(days=2)
        BookingFactory(swimmers=[swimmer], booked_at=base_start)

        test_datetime = base_start + timedelta(minutes=offset_minutes)

        payload = BookingQuery(
            booked_at=test_datetime,
            swimmers_ids=[swimmer.id],
        )
        with pytest.raises(BookingAlreadyTakenForSwimmerException):
            create_bookings_usecase(
                user.id, payload, user_repo, swimmer_repo, booking_repo
            )

    def test_create_booking_in_the_past(self, user_repo, swimmer_repo, booking_repo):
        user = UserFactory()
        swimmer = SwimmerFactory(link_user=user)
        datetime_booked_at = datetime.now(timezone.utc) - timedelta(days=2)

        payload = BookingQuery(
            booked_at=datetime_booked_at,
            swimmers_ids=[swimmer.id],
        )

        with pytest.raises(BookingMustBeInTheFutureException):
            create_bookings_usecase(
                user.id, payload, user_repo, swimmer_repo, booking_repo
            )
