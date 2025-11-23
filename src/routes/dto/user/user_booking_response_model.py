from pydantic import BaseModel
from src.routes.dto.booking.booking_dto import BookingDTO


class UserBookingResponseModel(BaseModel):
    user_first_name: str
    user_last_name: str
    user_email: str
    bookings: list[BookingDTO]
