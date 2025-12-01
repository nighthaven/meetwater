from pydantic import BaseModel, ConfigDict
from typing import List

from src.routes.dto.swimmer.swimmer_response_model import SwimmerResponseModel


class ListSwimmersResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    swimmers: List[SwimmerResponseModel]
