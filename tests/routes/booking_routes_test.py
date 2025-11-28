from src.models.booking import Booking
from tests.fixtures.swimmer_factory import SwimmerFactory
from tests.fixtures.swimming_coach_factory import SwimmingCoachFactory
from datetime import datetime, timezone, timedelta


class TestBookingRoutes:
    def test_booking_route(self, representative_client, db_session):
        swimmer = SwimmerFactory(representatives=[representative_client.user_type])
        swimming_coach = SwimmingCoachFactory()
        date_appointement = datetime.now(timezone.utc) + timedelta(days=1)
        payload = {
            "appointment_at": date_appointement.isoformat(),
            "swimmers_ids": [str(swimmer.id)],
            "swimming_coach_id": str(swimming_coach.id),
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
