from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel

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

class ListGrpResponse(BaseModel):
    id: int
    name: str
    updated_at: Optional[datetime] = None

class GetDebtResponse(BaseModel):
    owes_user_id: int
    owed_user_id: int
    amount: float
    currency_code: str

class PaymanSearchInput(BaseModel):
    name : Optional[str] = None
    contact_email : Optional[str] = None


class PaymanBalanceInput(BaseModel):
    currency_code: Literal['USD', 'USDC', 'TSD'] = 'USD'

class PaymanContactDetails(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
class PaymanCreatePayeeBase(BaseModel):
    type: Literal["PAYMAN_WALLET","CRYPTO_ADDRESS","US_ACH","TEST_RAILS"]
    name: str
    tags: Optional[List[str]] = None

class PaymanWalletPayee(PaymanCreatePayeeBase):
    payman_wallet_paytag: str

class PaymanCryptoPayee(PaymanCreatePayeeBase):
    address: str 
    chain: str 
    currency: str
    contact_details: Optional[PaymanContactDetails] = None

class PaymanTestPayee(PaymanCreatePayeeBase):
    pass