from uuid import UUID

from src.exceptions.booking.booking_not_found_exception import BookingNotFoundException
from src.models.booking import Booking
from src.repositories.booking_repository import BookingRepository


def get_and_validate_booking(
    booking_id: UUID, booking_repository: BookingRepository
) -> Booking:
    booking = booking_repository.find(booking_id)
    if not booking:
        raise BookingNotFoundException("booking not found")
    return booking
