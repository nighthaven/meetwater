from typing import List
from datetime import datetime, timezone, timedelta

from src.exceptions.swimming_coach.no_coach_available import NoCoachAvailable
from src.exceptions.swimming_coach.swimming_coach_already_have_an_appointement import (
    SwimmingCoachAlreadyHaveAnAppointement,
)
from src.exceptions.swimming_coach.swimming_coach_not_available import (
    SwimmingCoachNotAvailable,
)
from src.models.enums.coach_activity import CoachActivity
from src.models.enums.swimmer_level import SwimmerLevel
from src.models.swimmer import Swimmer
from src.models.swimming_coach import SwimmingCoach
from src.repositories.swimmer_repository import SwimmerRepository
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.routes.dto.booking.booking_query import BookingQuery
from src.usecases.booking.domain.planning_mapping import PLANNING_MAPPING
from src.usecases.validations.swimming_coach_validations import (
    get_and_validate_swimming_coach,
)


class CoachAssignationService:
    def __init__(self, booking_query: BookingQuery):
        self.booking_query = booking_query

    def assign_validate_and_return_swimming_coach(
        self,
        list_swimmers: List[Swimmer],
        swimmer_repository: SwimmerRepository,
        swimming_coach_repository: SwimmingCoachRepository,
    ) -> SwimmingCoach:
        is_adult_swimmer = list_swimmers[0].is_adult
        coach_planning_to_match = self.get_coach_activity(
            is_adult_swimmer, list_swimmers[0].level
        )

        appointment_at = self.booking_query.appointment_at
        duration_minutes = self.booking_query.duration_minutes
        swimming_coach_id = self.booking_query.swimming_coach_id
        if swimming_coach_id:
            return self._find_selected_swimming_coach(
                coach_planning_to_match,
                swimming_coach_repository,
            )
        else:
            coach = None

        list_coaches = [coach for swimmer in list_swimmers for coach in swimmer.coaches]
        if list_coaches:
            list_coaches = self._filter_schedule_for_coaches(
                list_coaches, coach_planning_to_match
            )
            list_coaches = self._filter_coach_without_appointement(list_coaches)
            coach = self._choose_coach(list_coaches)
        if not list_coaches or not coach:
            list_coaches = swimming_coach_repository.get_all_available_coach(
                appointment_at, duration_minutes, coach_planning_to_match
            )
            if not list_coaches:
                raise NoCoachAvailable()
            coach = self._choose_coach(list_coaches)
            if not coach:
                raise NoCoachAvailable()
        self._assign_coach_to_swimmer(list_swimmers, coach, swimmer_repository)
        return coach

    @staticmethod
    def get_coach_activity(is_adult: bool, level: SwimmerLevel) -> CoachActivity:
        try:
            return PLANNING_MAPPING[(is_adult, level)]
        except KeyError:
            raise ValueError(f"No coach planning defined for {is_adult=} {level=}")

    def _find_selected_swimming_coach(
        self,
        coach_planning_to_match: CoachActivity,
        swimming_coach_repository: SwimmingCoachRepository,
    ) -> SwimmingCoach:
        assert self.booking_query.swimming_coach_id is not None
        swimming_coach = get_and_validate_swimming_coach(
            self.booking_query.swimming_coach_id, swimming_coach_repository
        )

        appointment_at = self.booking_query.appointment_at
        duration_minutes = self.booking_query.duration_minutes
        for booking in swimming_coach.bookings:
            booking_over = booking.appointment_at + timedelta(
                minutes=booking.duration_minutes
            )
            if booking.appointment_at <= appointment_at < booking_over:
                raise SwimmingCoachAlreadyHaveAnAppointement(
                    "Coach already have an appointement at this time."
                )

        appointment_over = appointment_at + timedelta(minutes=duration_minutes)
        is_schedule_matching = False
        for schedule in swimming_coach.schedules:
            if (
                schedule.activity == coach_planning_to_match
                and appointment_at <= schedule.scheduled_at < appointment_over
            ):
                is_schedule_matching = True
        if not is_schedule_matching:
            raise SwimmingCoachNotAvailable("Coach not available.")
        return swimming_coach

    def _filter_schedule_for_coaches(
        self,
        list_coaches: List[SwimmingCoach],
        coach_activity: CoachActivity,
    ) -> List[SwimmingCoach]:
        appointment_at = self.booking_query.appointment_at
        appointment_over = appointment_at + timedelta(
            minutes=self.booking_query.duration_minutes
        )
        list_selected_coaches = []
        for coach in list_coaches:
            for schedule in coach.schedules:
                if (
                    schedule.activity == coach_activity
                    and appointment_at <= schedule.scheduled_at < appointment_over
                ):
                    list_selected_coaches.append(coach)
        return list_selected_coaches

    def _filter_coach_without_appointement(
        self, list_coaches: List[SwimmingCoach]
    ) -> List[SwimmingCoach]:
        appointment_at = self.booking_query.appointment_at
        appointment_over = appointment_at + timedelta(
            minutes=self.booking_query.duration_minutes
        )
        for coach in list_coaches:
            for booking in coach.bookings:
                if appointment_at <= booking.appointment_at < appointment_over:
                    list_coaches.remove(coach)
        return list_coaches

    @staticmethod
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

    @staticmethod
    def _assign_coach_to_swimmer(
        list_swimmers: List[Swimmer],
        coach: SwimmingCoach,
        swimmer_repository: SwimmerRepository,
    ) -> None:
        for swimmer in list_swimmers:
            swimmer.coaches.append(coach)
            swimmer_repository.save(swimmer)
