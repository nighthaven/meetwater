from fastapi import Depends

from src.models.link.swimmers_bookings import SwimmerBooking
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.services.security import Security
from src.models.booking import Booking

from src.models.representative import Representative
from src.repositories.booking_repository import BookingRepository
from src.repositories.swimmer_repository import SwimmerRepository
from src.routes.dto.booking.booking_query import BookingQuery
from src.usecases.booking.booking_services.coach_assignation_service import (
    CoachAssignationService,
)
from src.usecases.booking.booking_services.swimmer_verification_service import (
    SwimmerVerificationService,
)


def create_bookings_usecase(
    booking_query: BookingQuery,
    swimmer_repository: SwimmerRepository,
    booking_repository: BookingRepository,
    swimming_coach_repository: SwimmingCoachRepository,
    current_representative: Representative = Depends(
        Security.get_current_representative
    ),
) -> None:
    swimmer_verification_service = SwimmerVerificationService(
        current_representative.swimmers, booking_query
    )

    swimmer_verification_service.validate_representative_have_swimmers_and_query_contain_swimmer()
    selected_swimmers = swimmer_verification_service.check_and_return_selected_swimmer(
        swimmer_repository
    )

    coach_assignation_service = CoachAssignationService(booking_query)
    coach = coach_assignation_service.assign_validate_and_return_swimming_coach(
        selected_swimmers,
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
