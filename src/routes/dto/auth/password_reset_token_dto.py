from pydantic import BaseModel, EmailStr


class PasswordResetRequestDTO(BaseModel):
    email: EmailStr
