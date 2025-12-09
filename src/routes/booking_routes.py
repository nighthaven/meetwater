from fastapi import HTTPException
from typing import Annotated, Any, List

from fastapi import APIRouter, Depends, status

from src.exceptions.booking.booking_already_taken_for_swimmer_exception import (
    BookingAlreadyTakenForSwimmerException,
)
from src.exceptions.representative.representative_not_found_exception import (
    RepresentativeNotFoundException,
)
from src.exceptions.representative.representative_not_linked_to_swimmer_exception import (
    RepresentativeNotLinkedToSwimmerException,
)
from src.exceptions.swimmer.swimmer_not_found_exception import SwimmerNotFoundException
from src.exceptions.swimming_coach.swimming_coach_not_found_exception import (
    SwimmingCoachNotFoundException,
)
from src.models.representative import Representative
from src.repositories.booking_repository import BookingRepository
from src.repositories.swimmer_repository import SwimmerRepository
from src.repositories.swimming_coaches_repository import SwimmingCoachRepository
from src.routes.dto.booking.booking_response_model import BookingResponseModel
from src.routes.dto.booking.booking_query import BookingQuery
from src.services.security import Security
from src.usecases.booking.create_bookings import create_bookings_usecase
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
    current_representative: Representative = Depends(
        Security.get_current_representative
    ),
):
    try:
        create_bookings_usecase(
            query,
            swimmer_repository,
            booking_repository,
            swimming_coach_repository,
            current_representative,
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
    except SwimmingCoachNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Swimming coach not found"
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
            swimmers = [sb.swimmer for sb in booking.swimmers]
            serialized.append(
                BookingResponseModel.model_validate(
                    {
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
