from pydantic import BaseModel, EmailStr
from uuid import UUID


class PoolManagerQuery(BaseModel):
    first_name: str
    last_name: str
    swimming_pool_id: UUID
    email: EmailStr
    raw_password: str
