from typing import Optional

from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: Optional[str] = None
    representative_id: Optional[str] = None
    admin_id: Optional[str] = None
    pool_manager_id: Optional[str] = None
    swimming_coach_id: Optional[str] = None
