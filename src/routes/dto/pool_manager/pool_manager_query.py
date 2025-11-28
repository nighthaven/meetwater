from pydantic import BaseModel, EmailStr


class PoolManagerQuery(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    raw_password: str
