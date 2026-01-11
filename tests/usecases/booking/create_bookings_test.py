from datetime import timezone, date
from uuid import UUID

import pytest

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
from src.exceptions.swimming_coach.no_coach_available import NoCoachAvailable
from src.models.booking import Booking
from src.models.enums.coach_activity import CoachActivity
from src.models.enums.swimmer_level import SwimmerLevel
from src.routes.dto.booking.booking_query import BookingQuery
from src.services.date_time_service import DateTimeService
from src.usecases.booking.create_bookings import create_bookings_usecase
from tests.fixtures.booking_factory import BookingFactory
from tests.fixtures.coach_schedule_factory import CoachScheduleFactory
from tests.fixtures.swimmer_factory import SwimmerFactory
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory


class TestCreateBooking:
    def test_create_booking_with_coach_assignated(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimmer = SwimmerFactory(representatives=[authenticated_representative])
        swimming_coach = SwimmingCoachFactory(swimmers=[swimmer])
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)
        date_appointement = DateTimeService.futur_date_and_time(1, 14)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer.id],
        )

        create_bookings_usecase(
            query,
            swimmer_repo,
            booking_repo,
            swimming_coach_repo,
            authenticated_representative,
        )

        query_booking = db_session.query(Booking).all()
        assert len(query_booking) == 1
        assert query_booking[0].appointment_at == date_appointement
        assert query_booking[0].swimmers[0].swimmer.id == swimmer.id
        assert query_booking[0].swimming_coach_id == swimming_coach.id

    def test_create_booking_with_no_coach_assignated(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimmer = SwimmerFactory(representatives=[authenticated_representative])
        swimming_coach = SwimmingCoachFactory()
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)
        date_appointement = DateTimeService.futur_date_and_time(1, 14)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer.id],
        )

        create_bookings_usecase(
            query,
            swimmer_repo,
            booking_repo,
            swimming_coach_repo,
            authenticated_representative,
        )

        query_booking = db_session.query(Booking).all()
        assert len(query_booking) == 1
        assert query_booking[0].appointment_at == date_appointement
        assert query_booking[0].swimmers[0].swimmer.id == swimmer.id
        assert query_booking[0].swimming_coach_id == swimming_coach.id

    def test_create_booking_without_swimmers(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimming_coach = SwimmingCoachFactory()
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)
        date_appointement = DateTimeService.futur_date_and_time(1, 14)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[UUID("3e4bec05-cd91-4e91-b448-0948a53a2499")],
        )

        with pytest.raises(
            SwimmerNotFoundException,
            match="User need to create swimmer in order to book a session",
        ):
            create_bookings_usecase(
                query,
                swimmer_repo,
                booking_repo,
                swimming_coach_repo,
                authenticated_representative,
            )

    def test_create_booking_swimmer_not_assigned_to_representative(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        SwimmerFactory(representatives=[authenticated_representative])
        swimmer_not_owned_by_representative = SwimmerFactory()
        swimming_coach = SwimmingCoachFactory(
            swimmers=[swimmer_not_owned_by_representative]
        )
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)
        date_appointement = DateTimeService.futur_date_and_time(1, 14)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer_not_owned_by_representative.id],
        )

        with pytest.raises(
            RepresentativeNotLinkedToSwimmerException,
            match="Representative must add the swimmer first",
        ):
            create_bookings_usecase(
                query,
                swimmer_repo,
                booking_repo,
                swimming_coach_repo,
                authenticated_representative,
            )

    def test_create_booking_with_swimming_coach_who_already_have_booking_at_this_datetime(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimmer = SwimmerFactory(representatives=[authenticated_representative])
        date_appointement = DateTimeService.futur_date_and_time(1, 14)
        BookingFactory(swimmers=[swimmer], appointment_at=date_appointement)

        swimming_coach = SwimmingCoachFactory(swimmers=[swimmer])
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer.id],
        )

        with pytest.raises(
            BookingAlreadyTakenForSwimmerException,
            match="A booking already exist for this swimmer at this specific date and time",
        ):
            create_bookings_usecase(
                query,
                swimmer_repo,
                booking_repo,
                swimming_coach_repo,
                authenticated_representative,
            )

    def test_create_booking_no_coach_assignated_and_no_coach_available(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimmer = SwimmerFactory(representatives=[authenticated_representative])
        date_appointement = DateTimeService.futur_date_and_time(1, 14)
        schedule = CoachScheduleFactory.build(
            activity=CoachActivity.AQUA_BIKE, scheduled_at=date_appointement
        )
        swimming_coach = SwimmingCoachFactory(schedules=[schedule])
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer.id],
        )

        with pytest.raises(NoCoachAvailable, match="No coach available"):
            create_bookings_usecase(
                query,
                swimmer_repo,
                booking_repo,
                swimming_coach_repo,
                authenticated_representative,
            )

    def test_create_booking_no_coach_assignated_and_coach_available_because_of_booking(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimmer = SwimmerFactory(representatives=[authenticated_representative])
        date_appointement = DateTimeService.futur_date_and_time(1, 14)
        schedule = CoachScheduleFactory.build(scheduled_at=date_appointement)
        swimming_coach = SwimmingCoachFactory(schedules=[schedule])
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)
        BookingFactory(swimming_coach=swimming_coach, appointment_at=date_appointement)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer.id],
        )

        with pytest.raises(NoCoachAvailable, match="No coach available"):
            create_bookings_usecase(
                query,
                swimmer_repo,
                booking_repo,
                swimming_coach_repo,
                authenticated_representative,
            )

    def test_create_booking_with_coach_assignated_no_coach_available(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimmer = SwimmerFactory(representatives=[authenticated_representative])
        date_appointement = DateTimeService.futur_date_and_time(1, 14)
        schedule = CoachScheduleFactory.build(
            activity=CoachActivity.AQUA_BIKE, scheduled_at=date_appointement
        )
        swimming_coach = SwimmingCoachFactory(swimmers=[swimmer], schedules=[schedule])
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer.id],
        )

        with pytest.raises(NoCoachAvailable, match="No coach available"):
            create_bookings_usecase(
                query,
                swimmer_repo,
                booking_repo,
                swimming_coach_repo,
                authenticated_representative,
            )

    def test_create_booking_with_coach_assignated_no_coach_available_because_of_booking(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimmer = SwimmerFactory(representatives=[authenticated_representative])
        swimming_coach = SwimmingCoachFactory(swimmers=[swimmer])
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)
        date_appointement = DateTimeService.futur_date_and_time(1, 14)
        BookingFactory(swimming_coach=swimming_coach, appointment_at=date_appointement)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer.id],
        )

        with pytest.raises(NoCoachAvailable, match="No coach available"):
            create_bookings_usecase(
                query,
                swimmer_repo,
                booking_repo,
                swimming_coach_repo,
                authenticated_representative,
            )

    def test_create_booking_with_multiple_swimmers_not_same_level(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimmer_1 = SwimmerFactory(
            representatives=[authenticated_representative],
            level=SwimmerLevel.INTERMEDIATE,
        )
        swimmer_2 = SwimmerFactory(
            representatives=[authenticated_representative], level=SwimmerLevel.BEGINNER
        )
        swimming_coach = SwimmingCoachFactory(swimmers=[swimmer_1, swimmer_2])
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)
        date_appointement = DateTimeService.futur_date_and_time(1, 14)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer_1.id, swimmer_2.id],
        )

        with pytest.raises(
            SwimmersNotSameAgeOrLevel, match="swimmers not same age or level"
        ):
            create_bookings_usecase(
                query,
                swimmer_repo,
                booking_repo,
                swimming_coach_repo,
                authenticated_representative,
            )

    def test_create_booking_with_multiple_swimmers_not_same_age_categories(
        self,
        db_session,
        swimmer_repo,
        booking_repo,
        swimming_coach_repo,
        authenticated_representative,
    ):
        swimmer_adult = SwimmerFactory(
            representatives=[authenticated_representative],
            birth_date=date(date.today().year - 20, 1, 1),
        )
        swimmer_child = SwimmerFactory(
            representatives=[authenticated_representative],
            birth_date=date(date.today().year - 6, 1, 1),
        )
        swimming_coach = SwimmingCoachFactory(swimmers=[swimmer_adult, swimmer_child])
        for schedule in swimming_coach.schedules:
            schedule.scheduled_at = schedule.scheduled_at.astimezone(timezone.utc)
        date_appointement = DateTimeService.futur_date_and_time(1, 14)

        query = BookingQuery(
            appointment_at=date_appointement,
            swimmers_ids=[swimmer_adult.id, swimmer_child.id],
        )

        with pytest.raises(
            SwimmersNotSameAgeOrLevel, match="swimmers not same age or level"
        ):
            create_bookings_usecase(
                query,
                swimmer_repo,
                booking_repo,
                swimming_coach_repo,
                authenticated_representative,
            )
