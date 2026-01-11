from pydantic import BaseModel


class SwimmingCoachResponseModel(BaseModel):
    first_name: str
    last_name: str
