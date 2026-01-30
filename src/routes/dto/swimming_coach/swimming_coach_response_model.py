from pydantic import BaseModel, ConfigDict
from uuid import UUID


class SwimmingCoachResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
