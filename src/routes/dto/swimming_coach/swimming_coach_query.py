from pydantic import BaseModel, EmailStr
from datetime import date


class SwimmingCoachQuery(BaseModel):
    first_name: str
    last_name: str
    last_caep_certification_date: date
    last_pse_certification_date: date
    email: EmailStr
    raw_password: str
