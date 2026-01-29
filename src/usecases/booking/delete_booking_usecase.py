from uuid import UUID
from fastapi import Depends


from datetime import datetime, timezone, timedelta

from src.exceptions.booking.booking_cancellation_minimum_exception import (
    BookingCancellationMinimumException,
)
from src.models.user import User
from src.repositories.booking_repository import BookingRepository
from src.services.security import Security
from src.usecases.validations.get_and_validate_booking import get_and_validate_booking


def delete_booking_usecase(
    booking_id: UUID,
    booking_repository: BookingRepository,
    current_user: User = Depends(Security.get_current_user),
):
    booking = get_and_validate_booking(booking_id, booking_repository)

    now = datetime.now(timezone.utc)
    time_before_appointment = booking.appointment_at - now
    if current_user.representative and time_before_appointment < timedelta(hours=24):
        raise BookingCancellationMinimumException(
            "booking can't be cancelled if date is less than 24h"
        )

    booking_repository.delete(booking_id)
    return
