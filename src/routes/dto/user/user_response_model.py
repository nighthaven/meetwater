from pydantic import BaseModel
from typing import List

from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel


class UserResponseModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    swimmers: List[SwimmerResponseModel]
