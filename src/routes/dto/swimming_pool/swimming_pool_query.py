from pydantic import BaseModel


class SwimmingPoolQuery(BaseModel):
    pool_name: str
    address: str
    city: str
    post_code: str
