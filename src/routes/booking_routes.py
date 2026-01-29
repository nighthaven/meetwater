from fastapi import HTTPException
from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, status

from src.exceptions.booking.booking_already_taken_for_swimmer_exception import (
    BookingAlreadyTakenForSwimmerException,
)
from src.exceptions.booking.booking_cancellation_minimum_exception import (
    BookingCancellationMinimumException,
)
from src.exceptions.booking.booking_not_found_exception import BookingNotFoundException
from src.exceptions.representative.representative_not_found_exception import (
    RepresentativeNotFoundException,
)
from src.exceptions.representative.representative_not_linked_to_swimmer_exception import (
    RepresentativeNotLinkedToSwimmerException,
)
from src.exceptions.swimmer.swimmer_not_found_exception import SwimmerNotFoundException
from src.exceptions.swimmer.swimmers_not_same_age_or_level import (
    SwimmersNotSameAgeOrLevel,
)
from src.exceptions.swimming_coach.no_coach_available import NoCoachAvailable
from src.exceptions.swimming_coach.swimming_coach_not_found_exception import (
    SwimmingCoachNotFoundException,
)
from src.models.representative import Representative
from src.models.user import User
from src.repositories.booking_repository import BookingRepository
from src.repositories.swimmer_repository import SwimmerRepository
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.routes.dto.booking.booking_response_model import BookingResponseModel
from src.routes.dto.booking.booking_query import BookingQuery
from src.services.security import Security
from src.usecases.booking.create_bookings import create_bookings_usecase
from src.usecases.booking.delete_booking_usecase import delete_booking_usecase
from src.usecases.booking.get_bookings_by_representative_swimmers import (
    get_bookings_by_representative_swimmers,
)

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_booking(
    query: BookingQuery,
    swimmer_repository: Annotated[Any, Depends(SwimmerRepository)],
    booking_repository: Annotated[Any, Depends(BookingRepository)],
    swimming_coach_repository: Annotated[Any, Depends(SwimmingCoachRepository)],
    current_user: User = Depends(Security.get_current_user),
):
    try:
        create_bookings_usecase(
            query,
            swimmer_repository,
            booking_repository,
            swimming_coach_repository,
            current_user,
        )
    except RepresentativeNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not representative"
        )
    except SwimmerNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Swimmer not found"
        )
    except RepresentativeNotLinkedToSwimmerException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Swimmer not linked to representative",
        )
    except BookingAlreadyTakenForSwimmerException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A booking already exist for this swimmer at this specific date and time",
        )
    except SwimmersNotSameAgeOrLevel:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Swimmers don't have same group age or level",
        )
    except SwimmingCoachNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Swimming coach not found"
        )
    except NoCoachAvailable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No coach available"
        )


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[BookingResponseModel]
)
def get_bookings(
    booking_repository: Annotated[Any, Depends(BookingRepository)],
    current_representative: Representative = Depends(
        Security.get_current_representative
    ),
):
    try:
        bookings = get_bookings_by_representative_swimmers(
            booking_repository, current_representative
        )
        serialized = []
        for booking in bookings:
            swimmers = [
                swimmers_bookings.swimmer for swimmers_bookings in booking.swimmers
            ]
            serialized.append(
                BookingResponseModel.model_validate(
                    {
                        "id": booking.id,
                        **booking.__dict__,
                        "swimmers": swimmers,
                        "swimming_coach_name": (
                            booking.swimming_coach.full_name
                            if booking.swimming_coach
                            else None
                        ),
                    }
                )
            )

        return serialized
    except RepresentativeNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not representative"
        )


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id,
    booking_repository: Annotated[Any, Depends(BookingRepository)],
    current_user: User = Depends(Security.get_current_user),
):
    try:
        delete_booking_usecase(booking_id, booking_repository, current_user)
    except BookingNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found"
        )
    except BookingCancellationMinimumException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Booking can't be cancelled if less than 24h",
        )
