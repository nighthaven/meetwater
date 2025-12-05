from src.usecases.booking.get_bookings_by_representative_swimmers import (
    get_bookings_by_representative_swimmers,
)
from tests.fixtures.booking_factory import BookingFactory
from tests.fixtures.swimmer_factory import SwimmerFactory


class TestGetBookingsByRepresentativeSwimmers:
    def test_get_bookings_by_representative_swimmers_returns_a_list_of_bookings(
        self, booking_repo, authenticated_representative, db_session
    ):
        swimmer_1 = SwimmerFactory(representatives=[authenticated_representative])
        swimmer_2 = SwimmerFactory(representatives=[authenticated_representative])
        booking_1 = BookingFactory(swimmers=[swimmer_1, swimmer_2])
        booking_2 = BookingFactory(swimmers=[swimmer_1, swimmer_2])

        response = get_bookings_by_representative_swimmers(
            booking_repo, authenticated_representative
        )

        assert len(response) == 2
        assert response[0].appointment_at == booking_1.appointment_at
        assert response[0].status == booking_1.status
        assert response[0].duration_minutes == booking_1.duration_minutes
        assert swimmer_1.id in [
            swimmer_booking.swimmer_id for swimmer_booking in response[0].swimmers
        ]
        assert swimmer_2.id in [
            swimmer_booking.swimmer_id for swimmer_booking in response[0].swimmers
        ]
        assert response[0].swimming_coach == booking_1.swimming_coach

        assert response[1].appointment_at == booking_2.appointment_at
        assert response[1].status == booking_2.status
        assert response[1].duration_minutes == booking_2.duration_minutes
        assert swimmer_1.id in [
            swimmer_booking.swimmer_id for swimmer_booking in response[1].swimmers
        ]
        assert swimmer_2.id in [
            swimmer_booking.swimmer_id for swimmer_booking in response[1].swimmers
        ]
        assert response[1].swimming_coach == booking_2.swimming_coach
