from uuid import UUID
from pydantic import BaseModel


class SwimmingPoolCreatedResponseModel(BaseModel):
    id: UUID
    pool_name: str
    slug: str
