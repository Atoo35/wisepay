from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from dataclasses import dataclass
from ..services.splitwise_client import SplitwiseClientWrapper


class CurrentUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str    
    
@dataclass
class MyDeps:  
    client: SplitwiseClientWrapper

class ListGrpResponse(BaseModel):
    id: int
    name: str
    updated_at: Optional[datetime] = None

class GetDebtResponse(BaseModel):
    to_spliwise_id: int
    amount: int
    currency_code: str