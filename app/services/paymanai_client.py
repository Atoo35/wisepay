import paymanai
import os


class PaymanWrapper:
    def __init__(self):
        self.client = paymanai.Client(x_payman_api_secret=os.getenv('PAYMAN_API_KEY'))

    def get_all_payees(self,name:str=None ):
        try:
            payees = self.client.payments.search_payees(name=name)
            return payees
        except Exception as e:
            print(f"Error fetching payees: {e}")
            return None