from datetime import date

from pydantic import BaseModel, EmailStr


class UserQuery(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birth_date: date
