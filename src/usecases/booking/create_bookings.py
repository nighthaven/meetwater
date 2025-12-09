from uuid import UUID
from datetime import timedelta, datetime
from typing import List

from fastapi import Depends

from src.exceptions.representative.representative_not_linked_to_swimmer_exception import (
    RepresentativeNotLinkedToSwimmerException,
)
from src.models.link.swimmer_representative import SwimmerRepresentative
from src.models.link.swimmers_bookings import SwimmerBooking
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.services.security import Security
from src.exceptions.booking.booking_already_taken_for_swimmer_exception import (
    BookingAlreadyTakenForSwimmerException,
)
from src.exceptions.swimmer.swimmer_not_found_exception import SwimmerNotFoundException
from src.exceptions.swimming_coach.swimming_coach_not_found_exception import (
    SwimmingCoachNotFoundException,
)
from src.models.booking import Booking

from src.models.representative import Representative
from src.models.swimming_coach import SwimmingCoach
from src.repositories.booking_repository import BookingRepository
from src.repositories.swimmer_repository import SwimmerRepository
from src.routes.dto.booking.booking_query import BookingQuery
from src.usecases.validations.swimmer_validations import validate_and_return_swimmer


def create_bookings_usecase(
    booking_query: BookingQuery,
    swimmer_repository: SwimmerRepository,
    booking_repository: BookingRepository,
    swimming_coach_repository: SwimmingCoachRepository,
    current_representative: Representative = Depends(
        Security.get_current_representative
    ),
) -> None:
    _validate_representative_have_swimmers_and_query_contain_swimmer(
        current_representative.swimmers, booking_query.swimmers_ids
    )
    selected_swimmers = _check_and_return_selected_swimmer(
        booking_query.swimmers_ids,
        current_representative.swimmers,
        booking_query.appointment_at,
        swimmer_repository,
    )
    coach = _validate_and_return_swimming_coach(
        booking_query.swimming_coach_id, swimming_coach_repository
    )

    new_booking = Booking()
    new_booking.appointment_at = booking_query.appointment_at
    new_booking.swimmers = [
        SwimmerBooking(swimmer=swimmer, booking=new_booking)
        for swimmer in selected_swimmers
    ]
    new_booking.swimming_coach = coach

    booking_repository.save(new_booking)
    return


def _check_and_return_selected_swimmer(
    swimmers_ids: List[UUID],
    swimmers_representatives: List[SwimmerRepresentative],
    datetime_query: datetime,
    swimmer_repository: SwimmerRepository,
):
    selected_swimmers = []
    for selected in swimmers_ids:
        selected_swimmer = validate_and_return_swimmer(selected, swimmer_repository)
        _validate_swimmer_linked_to_representative(selected, swimmers_representatives)
        _validate_booking_not_taken_for_swimmer(
            selected_swimmer.bookings, datetime_query
        )
        selected_swimmers.append(selected_swimmer)
    return selected_swimmers


def _validate_representative_have_swimmers_and_query_contain_swimmer(
    swimmers_representatives: List[SwimmerRepresentative], query: List[UUID]
) -> None:
    if not swimmers_representatives or not query:
        raise SwimmerNotFoundException(
            "User need to create swimmer in order to book a session"
        )
    return


def _validate_swimmer_linked_to_representative(
    swimmer_id: UUID, swimmers_representatives: List[SwimmerRepresentative]
) -> None:
    representative_swimmer_ids = [
        swimmer.swimmer_id for swimmer in swimmers_representatives
    ]
    if swimmer_id not in representative_swimmer_ids:
        raise RepresentativeNotLinkedToSwimmerException(
            "Representative must add the swimmer first"
        )


def _validate_booking_not_taken_for_swimmer(
    swimmer_bookings: List[SwimmerBooking], datetime_query: datetime
) -> None:
    if not swimmer_bookings:
        return
    for link in swimmer_bookings:
        start_time = link.booking.appointment_at
        end_time = start_time + timedelta(minutes=link.booking.duration_minutes)
        if start_time <= datetime_query < end_time:
            raise BookingAlreadyTakenForSwimmerException(
                "A booking already exist for this swimmer at this specific date and time"
            )


def _validate_and_return_swimming_coach(
    coach_id: UUID, swimming_coach_repository: SwimmingCoachRepository
) -> SwimmingCoach:
    coach = swimming_coach_repository.get(coach_id)
    if not coach:
        raise SwimmingCoachNotFoundException("Coach not found")
    return coach
