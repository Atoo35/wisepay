from splitwise import Splitwise
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
    
    def get_debt_by_group(self, group_id: int):
        self._ensure_token_set()
        group = self.client.getGroup(group_id)
        return group.getSimplifiedDebts()
    
    def get_user(self, user_id: int):
        self._ensure_token_set()
        return self.client.getUser(user_id)