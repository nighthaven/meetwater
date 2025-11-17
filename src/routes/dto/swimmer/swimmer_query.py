from datetime import date

from pydantic import BaseModel

from src.models.enums.swimmer_level import SwimmerLevel


class SwimmerQuery(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    level: SwimmerLevel
