from fastapi import HTTPException
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.exceptions.booking.booking_already_taken_for_swimmer_exception import (
    BookingAlreadyTakenForSwimmerException,
)
from src.exceptions.swimmer.swimmer_not_found_exception import SwimmerNotFoundException
from src.exceptions.user.user_not_found_exception import UserNotFoundException
from src.exceptions.user.user_not_linked_to_swimmer_exception import (
    UserNotLinkedToSwimmerException,
)
from src.repository.booking_repository import BookingRepository
from src.repository.swimmer_repository import SwimmerRepository
from src.repository.user_repository import UserRepository
from src.routes.dto.booking.booking_query import BookingQuery
from src.routes.dto.swimmer.swimmer_query import SwimmerQuery
from src.routes.dto.user.user_query import UserQuery
from src.routes.dto.user.user_response_model import UserResponseModel
from src.services.security import Security
from src.usecases.create_bookings import create_bookings_usecase
from src.usecases.create_swimmer import create_swimmer_by_user_id
from src.usecases.create_user import create_user_usecase
from src.usecases.get_user import get_user_by_id_usecase

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    query: UserQuery,
    security: Annotated[Any, Depends(Security)],
    user_repository: Annotated[Any, Depends(UserRepository)],
):
    create_user_usecase(query, user_repository, security)
    return


@router.post("/{user_id}/swimmer", status_code=status.HTTP_201_CREATED)
def create_swimmer(
    user_id: UUID,
    query: SwimmerQuery,
    user_repository: Annotated[Any, Depends(UserRepository)],
):
    try:
        create_swimmer_by_user_id(user_id, query, user_repository)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseModel
)
def get_user_by_id(
    user_id: UUID,
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
):
    try:
        return get_user_by_id_usecase(user_id=user_id, user_repository=user_repository)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.post("/{user_id}/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(
    user_id: UUID,
    booking_query: BookingQuery,
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
    swimmer_repository: Annotated[SwimmerRepository, Depends(SwimmerRepository)],
    booking_repository: Annotated[BookingRepository, Depends(BookingRepository)],
):
    try:
        create_bookings_usecase(
            user_id,
            booking_query,
            user_repository,
            swimmer_repository,
            booking_repository,
        )
        return
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except SwimmerNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User don't have swimmer associated or selected swimmer not found",
        )
    except UserNotLinkedToSwimmerException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="that swimmer is not associated to the user",
        )
    except BookingAlreadyTakenForSwimmerException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="booking already taken"
        )
