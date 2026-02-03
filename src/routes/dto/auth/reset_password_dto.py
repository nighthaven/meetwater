from pydantic import BaseModel


class ResetPasswordDto(BaseModel):
    token: str
    new_password: str
