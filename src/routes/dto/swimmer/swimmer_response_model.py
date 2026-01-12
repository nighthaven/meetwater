from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date
from uuid import UUID

from src.models.enums.swimmer_level import SwimmerLevel
from src.routes.dto.swimming_coach.swimming_coach_response_model import (
    SwimmingCoachResponseModel,
)


class SwimmerResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    first_name: str
    last_name: str
    birth_date: date
    level: SwimmerLevel
    coaches: List[SwimmingCoachResponseModel]
