from uuid import UUID
from datetime import timedelta, datetime
from typing import List

from src.exceptions.booking.booking_already_taken_for_swimmer_exception import (
    BookingAlreadyTakenForSwimmerException,
)
from src.exceptions.swimmer.swimmer_not_found_exception import SwimmerNotFoundException
from src.exceptions.user.user_not_linked_to_swimmer_exception import (
    UserNotLinkedToSwimmerException,
)
from src.models.booking import Booking
from src.models.link.swimmer_user_link import SwimmerUserLink
from src.models.link.swimmers_bookings_link import SwimmerBookingLink
from src.repository.booking_repository import BookingRepository
from src.repository.swimmer_repository import SwimmerRepository
from src.repository.user_repository import UserRepository
from src.routes.dto.booking.booking_query import BookingQuery
from src.usecases.validations.swimmer_validations import validate_and_return_swimmer
from src.usecases.validations.user_validations import validate_and_return_user


def create_bookings_usecase(
    user_id: UUID,
    booking_query: BookingQuery,
    user_repository: UserRepository,
    swimmer_repository: SwimmerRepository,
    booking_repository: BookingRepository,
) -> None:
    user = validate_and_return_user(user_id, user_repository)
    _validate_user_have_swimmers_and_query_contain_swimmer(
        user.swimmers, booking_query.swimmers_ids
    )
    selected_swimmers = _check_and_return_selected_swimmer(
        booking_query.swimmers_ids,
        user.swimmers,
        booking_query.booked_at,
        swimmer_repository,
    )

    new_booking = Booking()
    new_booking.booked_at = booking_query.booked_at
    new_booking.swimmers = [
        SwimmerBookingLink(swimmer=swimmer, booking=new_booking)
        for swimmer in selected_swimmers
    ]

    booking_repository.save(new_booking)
    return


def _check_and_return_selected_swimmer(
    swimmers_ids: List[UUID],
    user_swimmers: List[SwimmerUserLink],
    datetime_query: datetime,
    swimmer_repository: SwimmerRepository,
):
    selected_swimmers = []
    for selected in swimmers_ids:
        selected_swimmer = validate_and_return_swimmer(selected, swimmer_repository)
        _validate_swimmer_linked_to_user(selected, user_swimmers)
        _validate_booking_not_taken_for_swimmer(
            selected_swimmer.bookings, datetime_query
        )
        selected_swimmers.append(selected_swimmer)
    return selected_swimmers


def _validate_user_have_swimmers_and_query_contain_swimmer(
    user_swimmer: List[SwimmerUserLink], query: List[UUID]
) -> None:
    if not user_swimmer or not query:
        raise SwimmerNotFoundException(
            "User need to create swimmer in order to book a session"
        )
    return


def _validate_swimmer_linked_to_user(
    swimmer_id: UUID, user_swimmers: List[SwimmerUserLink]
) -> None:
    user_swimmer_ids = [swimmer.swimmer_id for swimmer in user_swimmers]
    if swimmer_id not in user_swimmer_ids:
        raise UserNotLinkedToSwimmerException("User must add the swimmer first")


def _validate_booking_not_taken_for_swimmer(
    swimmer_bookings: List[SwimmerBookingLink], datetime_query: datetime
) -> None:
    for link in swimmer_bookings:
        start_time = link.booking.booked_at
        end_time = start_time + timedelta(minutes=link.booking.time_slot)
        if start_time <= datetime_query < end_time:
            raise BookingAlreadyTakenForSwimmerException(
                "A booking already exist for this swimmer at this specific date and time"
            )
