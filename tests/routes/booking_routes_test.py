from src.models.booking import Booking
from src.models.enums.coach_activity import CoachActivity
from tests.fixtures.booking_factory import BookingFactory
from tests.fixtures.coach_schedule_factory import CoachScheduleFactory
from tests.fixtures.swimmer_factory import SwimmerFactory
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory
from datetime import datetime, timezone, timedelta


class TestBookingRoutes:
    def test_create_booking_route(self, representative_client, db_session):
        swimmer = SwimmerFactory(representatives=[representative_client.user_type])
        swimming_coach = SwimmingCoachFactory()
        date_appointement = datetime.now(timezone.utc) + timedelta(days=1)
        CoachScheduleFactory(
            activity=CoachActivity.CHILD_INTERMEDIATE,
            scheduled_at=date_appointement - timedelta(minutes=10),
            duration_minutes=300,
            swimming_coach=swimming_coach,
        )

        payload = {
            "appointment_at": date_appointement.isoformat(),
            "swimmers_ids": [str(swimmer.id)],
            "swimming_coach_id": None,
        }
        response = representative_client.post("/bookings", json=payload)

        assert response.status_code == 201
        query_booking = db_session.query(Booking).all()
        assert len(query_booking) == 1
        assert (
            query_booking[0].appointment_at.astimezone(timezone.utc)
            == date_appointement
        )
        assert query_booking[0].swimmers[0].swimmer.id == swimmer.id
        assert query_booking[0].swimming_coach_id == swimming_coach.id


class TestGetBookingRoute:
    def test_get_booking_route(self, representative_client, db_session):
        swimmer = SwimmerFactory(representatives=[representative_client.user_type])
        swimming_coach = SwimmingCoachFactory()
        booking_1 = BookingFactory(swimmers=[swimmer], swimming_coach=swimming_coach)
        booking_2 = BookingFactory(swimmers=[swimmer])

        response = representative_client.get("/bookings")

        assert response.status_code == 200
        assert (
            response.json()[0]["appointment_at"] == booking_1.appointment_at.isoformat()
        )
        assert response.json()[0]["duration_minutes"] == booking_1.duration_minutes
        assert response.json()[0]["status"] == booking_1.status
        assert (
            response.json()[0]["swimmers"][0]["first_name"]
            == booking_1.swimmers[0].swimmer.first_name
        )
        assert (
            response.json()[0]["swimming_coach_name"]
            == booking_1.swimming_coach.full_name
        )
        assert (
            response.json()[1]["appointment_at"] == booking_2.appointment_at.isoformat()
        )
        assert response.json()[1]["duration_minutes"] == booking_2.duration_minutes
        assert response.json()[1]["status"] == booking_2.status
        assert (
            response.json()[1]["swimmers"][0]["first_name"]
            == booking_2.swimmers[0].swimmer.first_name
        )
        assert (
            response.json()[1]["swimming_coach_name"]
            == booking_2.swimming_coach.full_name
        )
