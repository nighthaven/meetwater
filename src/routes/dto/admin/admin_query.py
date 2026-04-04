from pydantic import BaseModel, EmailStr


class AdminQuery(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    raw_password: str
