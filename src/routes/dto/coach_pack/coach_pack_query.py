from pydantic import BaseModel


class CoachPackQuery(BaseModel):
    sessions_count: int
    price: int
    final_price: int
