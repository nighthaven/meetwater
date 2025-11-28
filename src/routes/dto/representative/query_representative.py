from pydantic import BaseModel, EmailStr
from datetime import date


class QueryRepresentative(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    email: EmailStr
    raw_password: str
