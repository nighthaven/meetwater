from datetime import date

from pydantic import BaseModel, EmailStr

from src.models.enums.user_level import UserLevel
from typing import Optional


class UserQuery(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birth_date: date
    level: UserLevel
    representative: Optional[str] = None
