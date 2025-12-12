from uuid import UUID
from datetime import timedelta, datetime, timezone
from typing import List

from fastapi import Depends

from src.exceptions.representative.representative_not_linked_to_swimmer_exception import (
    RepresentativeNotLinkedToSwimmerException,
)
from src.exceptions.swimming_coach.no_coach_available import NoCoachAvailable
from src.models.enums.coach_activity import CoachActivity
from src.models.link.swimmer_representative import SwimmerRepresentative
from src.models.link.swimmers_bookings import SwimmerBooking
from src.models.swimmer import Swimmer
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.services.security import Security
from src.exceptions.booking.booking_already_taken_for_swimmer_exception import (
    BookingAlreadyTakenForSwimmerException,
)
from src.exceptions.swimmer.swimmer_not_found_exception import SwimmerNotFoundException
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
    coach = _assign_validate_and_return_swimming_coach(
        selected_swimmers,
        booking_query.appointment_at,
        booking_query.duration_minutes,
        swimmer_repository,
        swimming_coach_repository,
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


def _assign_validate_and_return_swimming_coach(
    list_swimmers: List[Swimmer],
    appointement_at: datetime,
    duration_minutes: int,
    swimmer_repository: SwimmerRepository,
    swimming_coach_repository: SwimmingCoachRepository,
) -> SwimmingCoach:
    list_coaches = [coach for swimmer in list_swimmers for coach in swimmer.coaches]
    coach = None
    if list_coaches:
        list_coaches = _filter_schedule_for_coaches(
            list_coaches, appointement_at, duration_minutes
        )
        list_coaches = _filter_coach_without_appointement(
            list_coaches, appointement_at, duration_minutes
        )
        coach = _choose_coach(list_coaches)
    if not list_coaches or not coach:
        list_coaches = swimming_coach_repository.get_all_available_coach(
            appointement_at, duration_minutes
        )
        if not list_coaches:
            raise NoCoachAvailable()
        coach = _choose_coach(list_coaches)
        if not coach:
            raise NoCoachAvailable()
    _assign_coach_to_swimmer(list_swimmers, coach, swimmer_repository)
    return coach


def _filter_schedule_for_coaches(
    list_coaches: List[SwimmingCoach],
    appointement_at: datetime,
    duration_minutes: int,
) -> List[SwimmingCoach]:
    appointment_over = appointement_at + timedelta(minutes=duration_minutes)
    list_selected_coaches = []
    for coach in list_coaches:
        for schedule in coach.schedules:
            if (
                schedule.activity == CoachActivity.AVAILABLE
                and appointement_at <= schedule.scheduled_at < appointment_over
            ):
                list_selected_coaches.append(coach)
    return list_selected_coaches


def _filter_coach_without_appointement(
    list_coaches: List[SwimmingCoach], appointement_at: datetime, duration_minutes: int
) -> List[SwimmingCoach]:
    appointment_over = appointement_at + timedelta(minutes=duration_minutes)
    for coach in list_coaches:
        for booking in coach.bookings:
            if appointement_at <= booking.appointment_at < appointment_over:
                list_coaches.remove(coach)
    return list_coaches


def _choose_coach(list_coach: List[SwimmingCoach]) -> SwimmingCoach | None:
    choosen_coach = None
    min_schedule = None
    for coach in list_coach:
        total_futur_schedule = len(
            [
                schedule
                for schedule in coach.schedules
                if schedule.scheduled_at >= datetime.now(timezone.utc)
            ]
        )
        if not min_schedule or total_futur_schedule < min_schedule:
            min_schedule = total_futur_schedule
            choosen_coach = coach

    return choosen_coach


def _assign_coach_to_swimmer(
    list_swimmers: List[Swimmer],
    coach: SwimmingCoach,
    swimmer_repository: SwimmerRepository,
) -> None:
    for swimmer in list_swimmers:
        swimmer.coaches.append(coach)
        swimmer_repository.save(swimmer)
