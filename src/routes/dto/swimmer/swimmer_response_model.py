from pydantic import BaseModel
from datetime import date

from src.models.enums.swimmer_level import SwimmerLevel


class SwimmerResponseModel(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    level: SwimmerLevel
