import paymanai
import os

from app.models.models import PaymanBalanceInput, PaymanSearchInput,PaymanCryptoPayee, PaymanTestPayee, PaymanWalletPayee


class PaymanWrapper:
    def __init__(self):
        self.client = paymanai.Client(x_payman_api_secret=os.getenv('PAYMAN_API_KEY'))

    def get_all_payees(self,input: PaymanSearchInput=None):
        try:
            payees = self.client.payments.search_payees(name=input.name,contact_email=input.contact_email)
            return payees
        except Exception as e:
            print(f"Error fetching payees: {e}")
            return None
        
    def get_balance(self, input: PaymanBalanceInput):
        try:
            balance = self.client.balances.get_spendable_balance(input.currency_code)
            return balance
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None
        
    def create_payee(self, input: PaymanCryptoPayee | PaymanWalletPayee | PaymanTestPayee):
        print(input)
        try:
            payee = self.client.payments.create_payee(**input.model_dump(exclude_none=True))
            return payee
        except Exception as e:
            print(f"Error creating payee: {e}")
