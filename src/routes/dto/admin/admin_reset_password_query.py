from pydantic import BaseModel, EmailStr


class AdminResetPasswordQuery(BaseModel):
    email: EmailStr
    new_password: str
