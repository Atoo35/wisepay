from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from dataclasses import dataclass

from app.services.paymanai_client import PaymanWrapper
from ..services.splitwise_client import SplitwiseClientWrapper

class SplitwiseUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

class CurrentUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str    
    
@dataclass
class MyDeps:  
    splitwise_client: SplitwiseClientWrapper
    payman_client: PaymanWrapper

class ListGrpResponse(BaseModel):
    id: int
    name: str
    updated_at: Optional[datetime] = None

class GetDebtResponse(BaseModel):
    owes_user_id: int
    owed_user_id: int
    amount: float
    currency_code: str