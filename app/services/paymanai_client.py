from typing import Dict, Optional
import paymanai
from paymanai.types import PaymentSendPaymentResponse
from ..config import settings
import os

from app.models.models import PaymanBalanceInput, PaymanSearchInput,PaymanCryptoPayee, PaymanTestPayee, PaymanWalletPayee


class PaymanWrapper:
    def __init__(self):
        self.client = paymanai.Client(x_payman_api_secret=settings.PAYMAN_API_KEY)

    def get_all_payees(self,input: PaymanSearchInput=None):
        try:
            payees = self.client.payments.search_payees(name=input.name,contact_email=input.contact_email)
            return payees
        except Exception as e:
            print(f"Error fetching payees: {e}")
            raise e
        
    def get_balance(self, input: PaymanBalanceInput):
        try:
            balance = self.client.balances.get_spendable_balance(input.currency_code)
            return balance
        except Exception as e:
            print(f"Error fetching balance: {e}")
            raise e
        
    def create_payee(self, input: PaymanCryptoPayee | PaymanWalletPayee | PaymanTestPayee):
        try:
            payee = self.client.payments.create_payee(**input.model_dump(exclude_none=True))
            return payee
        except Exception as e:
            print(f"Error creating payee: {e}")
            raise e

    def send_payment(self,amount:float,payee_id:str) -> str:
        try:
            tx = self.client.payments.send_payment(amount_decimal=amount,payee_id=payee_id)
            return tx.model_dump_json()
        except Exception as e:
            print(f'Error sending payment: {e}')
            raise e
