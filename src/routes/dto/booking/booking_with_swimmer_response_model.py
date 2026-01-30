from typing import List
from src.routes.dto.booking.booking_response_model import BookingResponseModel
from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel


class BookingWithSwimmersResponseModel(BookingResponseModel):
    swimmers: List[SwimmerResponseModel]
