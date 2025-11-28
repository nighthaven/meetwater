from pydantic import BaseModel, EmailStr
from typing import List

from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel


class UserResponseModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    swimmers: List[SwimmerResponseModel]
    is_coach: bool
