# app/db/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: str
    oauth_token: str
    splitwise_id: Optional[int]
    payman_id: Optional[str]  = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime] = None

class UserUpsert(BaseModel):
    email: str
    splitwise_id: Optional[int] = None
    oauth_token: Optional[str] = None
    payman_id: Optional[str] = None
