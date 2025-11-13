from pydantic import BaseModel


class UserResponseModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    representative: str
