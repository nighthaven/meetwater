from pydantic import BaseModel, ConfigDict
from datetime import time


class SwimmingPoolScheduleResponseModel(BaseModel):
    id: str
    day_of_week: str
    opening_time: time
    closing_time: time

    model_config = ConfigDict(from_attributes=True)
