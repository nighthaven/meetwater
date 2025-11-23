from uuid import UUID
from src.repository.user_repository import UserRepository
from src.usecases.validations.user_validations import validate_and_return_user


def get_bookings_by_user_id(user_id: UUID, user_repository: UserRepository):
    user = validate_and_return_user(user_id, user_repository)
    bookings = user_repository.get_bookings(user_id)
    return {
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
        "bookings": [
            {
                "id": booking.id,
                "booked_at": booking.booked_at,
                "created_at": booking.created_at,
                "time_slot": booking.time_slot,
                "status": booking.status,
                "swimmers": [
                    {
                        "id": swimmer.swimmer.id,
                        "first_name": swimmer.swimmer.first_name,
                        "last_name": swimmer.swimmer.last_name,
                        "birth_date": swimmer.swimmer.birth_date,
                        "level": swimmer.swimmer.level,
                    }
                    for swimmer in booking.swimmers
                ],
            }
            for booking in bookings
        ],
    }
