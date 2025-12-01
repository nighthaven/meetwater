from pydantic import BaseModel, ConfigDict
from datetime import date

from src.models.enums.swimmer_level import SwimmerLevel


class SwimmerResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    birth_date: date
    level: SwimmerLevel
