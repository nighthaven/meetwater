from datetime import datetime, timezone, timedelta

from src.models.swimming_coach import SwimmingCoach
from tests.fixtures.booking_factory import BookingFactory
from tests.fixtures.coach_pack_factory import CoachPackFactory
from tests.fixtures.coach_schedule_factory import CoachScheduleFactory
from tests.fixtures.swimming_pool_factory import SwimmingPoolFactory


class TestSwimmingCoachRoutes:
    def test_create_swimming_coach_as_admin(self, admin_client, db_session):
        swimming_pool = SwimmingPoolFactory()
        db_session.commit()
        caep_date = (datetime.now(timezone.utc) - timedelta(days=2 * 365)).date()
        pse_date = (datetime.now(timezone.utc) - timedelta(days=200)).date()
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "last_caep_certification_date": caep_date.isoformat(),
            "last_pse_certification_date": pse_date.isoformat(),
            "email": "johndoe_admin@example.com",
            "raw_password": "password",
            "swimming_pool_id": str(swimming_pool.id),
        }
        response = admin_client.post("/swimming_coaches/", json=payload)
        assert response.status_code == 201
        query_swimming_coach = db_session.query(SwimmingCoach).all()
        assert len(query_swimming_coach) == 1
        assert query_swimming_coach[0].first_name == "John"

    def test_create_swimming_coach_as_admin_without_pool_id_fails(
        self, admin_client, db_session
    ):
        caep_date = (datetime.now(timezone.utc) - timedelta(days=2 * 365)).date()
        pse_date = (datetime.now(timezone.utc) - timedelta(days=200)).date()
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "last_caep_certification_date": caep_date.isoformat(),
            "last_pse_certification_date": pse_date.isoformat(),
            "email": "johndoe_admin@example.com",
            "raw_password": "password",
        }
        response = admin_client.post("/swimming_coaches/", json=payload)
        assert response.status_code == 400

    def test_create_swimming_coach_routes(self, pool_manager_client, db_session):
        caep_date = (datetime.now(timezone.utc) - timedelta(days=2 * 365)).date()
        pse_date = (datetime.now(timezone.utc) - timedelta(days=200)).date()
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "last_caep_certification_date": caep_date.isoformat(),
            "last_pse_certification_date": pse_date.isoformat(),
            "email": "johndoe@example.com",
            "raw_password": "password",
        }
        response = pool_manager_client.post("/swimming_coaches/", json=payload)
        assert response.status_code == 201
        query_swimming_coach = db_session.query(SwimmingCoach).all()
        assert len(query_swimming_coach) == 1
        assert query_swimming_coach[0].first_name == "John"
        assert query_swimming_coach[0].last_name == "Doe"
        assert query_swimming_coach[0].last_caep_certification_date == caep_date
        assert query_swimming_coach[0].last_pse_certification_date == pse_date
        assert query_swimming_coach[0].user.email == "johndoe@example.com"

    def test_get_swimming_coach_route(self, swimming_coach_client, db_session):
        swimming_coach = swimming_coach_client.user_type
        CoachScheduleFactory(swimming_coach=swimming_coach)
        booking = BookingFactory(swimming_coach=swimming_coach)
        pack = CoachPackFactory(swimming_coach=swimming_coach)

        response = swimming_coach_client.get(
            "/swimming_coaches/", params={"swimming_coach_id": str(swimming_coach.id)}
        )
        assert response.status_code == 200
        assert response.json()["id"] == str(swimming_coach.id)
        assert response.json()["first_name"] == swimming_coach.first_name
        assert response.json()["last_name"] == swimming_coach.last_name
        assert response.json()["schedules"][0]["id"] == str(
            swimming_coach.schedules[0].id
        )
        assert (
            response.json()["schedules"][0]["activity"]
            == swimming_coach.schedules[0].activity.value
        )
        assert response.json()["schedules"][0]["scheduled_at"] == str(
            swimming_coach.schedules[0].scheduled_at.isoformat()
        )
        assert (
            response.json()["schedules"][0]["duration_minutes"]
            == swimming_coach.schedules[0].duration_minutes
        )
        assert response.json()["students"][0]["id"] == str(
            swimming_coach.students[0].id
        )
        assert (
            response.json()["students"][0]["first_name"]
            == swimming_coach.students[0].first_name
        )
        assert (
            response.json()["students"][0]["last_name"]
            == swimming_coach.students[0].last_name
        )
        assert (
            response.json()["students"][0]["birth_date"]
            == swimming_coach.students[0].birth_date.isoformat()
        )
        assert (
            response.json()["students"][0]["level"]
            == swimming_coach.students[0].level.value
        )
        assert response.json()["bookings"][0]["id"] == str(booking.id)
        assert (
            response.json()["bookings"][0]["appointment_at"]
            == booking.appointment_at.isoformat()
        )
        assert (
            response.json()["bookings"][0]["duration_minutes"]
            == booking.duration_minutes
        )
        assert (
            response.json()["bookings"][0]["swimming_coach_name"]
            == booking.swimming_coach.full_name
        )
        assert response.json()["coach_packs"][0]["id"] == str(pack.id)
        assert (
            response.json()["coach_packs"][0]["sessions_count"] == pack.sessions_count
        )
        assert response.json()["coach_packs"][0]["price"] == pack.price
        assert response.json()["coach_packs"][0]["final_price"] == pack.final_price
        assert response.json()["coach_packs"][0]["active"] == pack.active
