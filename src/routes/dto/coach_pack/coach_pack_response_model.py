from uuid import UUID
from pydantic import BaseModel


class CoachPackResponseModel(BaseModel):
    id: UUID
    sessions_count: int
    price: int
    final_price: int
    active: bool
