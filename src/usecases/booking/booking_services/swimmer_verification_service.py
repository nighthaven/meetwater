from uuid import UUID
from typing import List
from datetime import datetime, timedelta

from src.exceptions.booking.booking_already_taken_for_swimmer_exception import (
    BookingAlreadyTakenForSwimmerException,
)
from src.exceptions.representative.representative_not_linked_to_swimmer_exception import (
    RepresentativeNotLinkedToSwimmerException,
)
from src.exceptions.swimmer.swimmer_not_found_exception import SwimmerNotFoundException
from src.exceptions.swimmer.swimmers_not_same_age_or_level import (
    SwimmersNotSameAgeOrLevel,
)
from src.models.link.swimmer_representative import SwimmerRepresentative
from src.models.link.swimmers_bookings import SwimmerBooking
from src.models.swimmer import Swimmer
from src.repositories.swimmer_repository import SwimmerRepository
from src.routes.dto.booking.booking_query import BookingQuery
from src.usecases.validations.swimmer_validations import validate_and_return_swimmer


class SwimmerVerificationService:
    def __init__(
        self,
        swimmers_representatives: List[SwimmerRepresentative],
        booking_query: BookingQuery,
    ):
        self.swimmers_representatives = swimmers_representatives
        self.booking_query = booking_query

    def check_and_return_selected_swimmer(
        self,
        swimmer_repository: SwimmerRepository,
    ):
        selected_swimmers = []
        for selected in self.booking_query.swimmers_ids:
            selected_swimmer = validate_and_return_swimmer(selected, swimmer_repository)
            self._validate_swimmer_linked_to_representative(selected)
            self._validate_booking_not_taken_for_swimmer(
                selected_swimmer.bookings, self.booking_query.appointment_at
            )
            selected_swimmers.append(selected_swimmer)
        self._validate_selected_swimmer_same_age_and_level(selected_swimmers)
        return selected_swimmers

    def _validate_selected_swimmer_same_age_and_level(
        self, swimmers: List[Swimmer]
    ) -> None:
        level_first_swimmer = swimmers[0].level
        is_adult_first_swimmer = swimmers[0].is_adult
        for swimmer in swimmers:
            if (
                swimmer.level != level_first_swimmer
                or swimmer.is_adult != is_adult_first_swimmer
            ):
                raise SwimmersNotSameAgeOrLevel("swimmers not same age or level")
        return

    def validate_representative_have_swimmers_and_query_contain_swimmer(self) -> None:
        if not self.swimmers_representatives or not self.booking_query:
            raise SwimmerNotFoundException(
                "User need to create swimmer in order to book a session"
            )
        return

    def _validate_swimmer_linked_to_representative(
        self,
        swimmer_id: UUID,
    ) -> None:
        representative_swimmer_ids = [
            swimmer.swimmer_id for swimmer in self.swimmers_representatives
        ]
        if swimmer_id not in representative_swimmer_ids:
            raise RepresentativeNotLinkedToSwimmerException(
                "Representative must add the swimmer first"
            )

    @staticmethod
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
