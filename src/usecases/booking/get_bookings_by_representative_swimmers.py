from typing import List
from src.models.booking import Booking
from src.models.representative import Representative
from src.repositories.booking_repository import BookingRepository


def get_bookings_by_representative_swimmers(
    booking_repository: BookingRepository, current_representative: Representative
) -> List[Booking]:
    swimmers_representatives = current_representative.swimmers
    list_swimmer_ids = [
        swimmers_representative.swimmer.id
        for swimmers_representative in swimmers_representatives
    ]
    test = booking_repository.get_bookings_by_swimmers(list_swimmer_ids)
    return test
