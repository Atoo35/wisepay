import os
from pydantic_ai import RunContext
from splitwise import Splitwise
# from splitwise.user import User, Friend, CurrentUser

# from app.db.schemas import GetDebtResponse, ListGrpResponse
# from dotenv import load_dotenv
# import logging
# logging.basicConfig(level=logging.DEBUG)
    
class SplitwiseClientWrapper:
    def __init__(self, api_key, api_secret):
        self.client = Splitwise(api_key, api_secret)
        self.token_set = False

    def set_token(self, token: dict):
        self.client.setOAuth2AccessToken(token)
        self.token_set = True

    def _ensure_token_set(self):
        if not self.token_set:
            raise Exception("OAuth token not set on Splitwise client.")

    def get_current_user(self):
        self._ensure_token_set()
        return self.client.getCurrentUser()

    def get_groups(self):
        self._ensure_token_set()
        return self.client.getGroups()


# class SplitwiseUser:
#     def __init__(self, access_token: dict = None):
#         self.client = Splitwise(os.getenv('SPLITWISE_API_KEY'), os.getenv('SPLITWISE_API_SECRET'))
#         if access_token:
#             try:
#                 self.client.setOAuth2AccessToken(access_token)
#             except Exception as e:
#                 print(f'Error setting access token: {e}')
#                 raise e

#     def init_auth(self):
#         return self.client.getOAuth2AuthorizeURL(os.getenv('REDIRECT_URI'))

#     def fetch_access_token(self, code):
#         return self.client.getOAuth2AccessToken(code, os.getenv('REDIRECT_URI'))
    
   

#     @pydantic_agent.tool
#     def get_current_user(ctx: RunContext[None],self) -> CurrentUser:
#         current_user = ctx.client.getCurrentUser()
#         return CurrentUser(
#             id=current_user.getId(),
#             first_name=current_user.getFirstName(),
#             last_name=current_user.getLastName(),
#             email=current_user.getEmail()
#         )
    
#     def get_groups(self):
#         if not self.client:
#             raise ValueError("Client not initialized. Please login first.")
#         groups = self.client.getGroups()
#         res = list[ListGrpResponse]()
#         for group in groups:
#             id=group.getId()
#             name=group.getName()
#             updated_at=group.getUpdatedAt()
#             res.append(ListGrpResponse(id=id, name=name, updated_at=updated_at))
#         return res
    
#     def get_my_debt(self, group_id: int, user_id: int):
#         group = self.client.getGroup(group_id)
#         print(f"Group ID: {group_id}")
#         simplified_debts = group.getSimplifiedDebts()
#         for debt in simplified_debts:
#             from_user = debt.getFromUser()
#             if from_user == user_id:
#                 to_user = debt.getToUser()
#                 amount = debt.getAmount()
#                 currency_code = debt.getCurrencyCode()
#                 return GetDebtResponse(to_spliwise_id=to_user, amount=amount, currency_code=currency_code)
#         return None
    
#     def get_all_debts(self,user_id: int):
#         if not self.client:
#             raise ValueError("Client not initialized. Please login first.")
#         groups = self.get_groups()
#         res = list[GetDebtResponse]()
#         for group in groups:
#             debt=self.get_my_debt(group.id, user_id)
#             if debt:
#                 res.append(debt)
#         return res



        # return access_token
# url, secret = sObj.getOAuth2AuthorizeURL('http://localhost:8080')
# print(f'url:{url}')
# print(f'secret:{secret}')
# access_token = sObj.getOAuth2AccessToken('nzxjzlDUxR5ReCewVg8f','http://localhost:8080')
# print(access_token)
# sObj.setOAuth2AccessToken({'access_token': 'BPmceO68UiI7mPvvbAUsqPktWHYQnThdmhWhmcyz', 'token_type': 'bearer'})
# friends = sObj.getFriends()
# for friend in friends:
#     print(f"Name: {friend.getFirstName()} {friend.getLastName()}, Email: {friend.getEmail()}, ID: {friend.getId()}")

# groups = sObj.getGroups()
# for group in groups:
#     id=group.getId()
#     print(f"Group Name: {group.getName()}")
#     group = sObj.getGroup(id)
#     print(f"Group ID: {id}")
#     simplified_debts = group.getSimplifiedDebts()
#     for debt in simplified_debts:
#         print(f"from: {debt.getFromUser()}, to: {debt.getToUser()}, amount: {debt.getAmount()}, currency: {debt.getCurrencyCode()}")

#     print()
#     print()
#     original_debts = group.getOriginalDebts()
#     for debt in original_debts:
#         print(f"from: {debt.getFromUser()}, to: {debt.getToUser()}, amount: {debt.getAmount()}, currency: {debt.getCurrencyCode()}")
    # print(f'original debt:{group.getOriginalDebts()}')
#Store secret so you can retrieve it later
#redirect user to url

# http://localhost:8080/?code=nzxjzlDUxR5ReCewVg8f&state=hqxPsNaOyyvaS2UFYQ3hyo2hceDy8W