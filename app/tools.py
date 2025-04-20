import json
from typing import List

from .db.dao import get_user_by_id
from .services.ai import pydantic_agent
from .models.models import CurrentUser, GetDebtResponse, ListGrpResponse, MyDeps,SplitwiseUser
from pydantic_ai import RunContext

@pydantic_agent.tool
def set_access_token(ctx: RunContext[MyDeps], oauth_token: str) -> None:
    """
   Set the access token for the Splitwise client.
    This MUST be called after get_user_by_id() and before any other Splitwise functions.

    Args:
        ctx: The context object containing the Splitwise client.
        oauth_token: This is a dictionary containing the access token and other information. use it as is

    Returns:
        None: This function does not return anything.
    """
    try:
        # convert the str to dictionary maybe using json.loads
        token_dict = json.loads(oauth_token)
        ctx.deps.client.set_token(token_dict)
    except Exception as e:
        print(f'Error setting access token: {e}')
        raise e

@pydantic_agent.tool
def get_current_user(ctx: RunContext[MyDeps]) -> CurrentUser:
    """
    Get the current user from the Splitwise client.
    This function retrieves the current user's information from Splitwise.
    
    Args:
        ctx: The context object containing the Splitwise client.

    Returns:
        CurrentUser: The current user's information.
    """
    try:
        current_user = ctx.deps.client.get_current_user()
        return CurrentUser(
            id=current_user.getId(),
            first_name=current_user.getFirstName(),
            last_name=current_user.getLastName(),
            email=current_user.getEmail()
        )
    except Exception as e:
        print(f'Error getting current user: {e}')
        raise e
    
@pydantic_agent.tool
def get_user_groups(ctx: RunContext[MyDeps]) -> List[ListGrpResponse]:
    """
    Get the groups of the current user from the Splitwise client.
    This function retrieves the groups that the current user is a member of.

    Args:
        ctx: The context object containing the Splitwise client.

    Returns:
        ListGrpResponse: A response object containing the groups that the current user is a member of.
    """
    try:
        groups = ctx.deps.client.get_groups()
        return [
            ListGrpResponse(
                id=group.getId(),
                name=group.getName(),
                updated_at=group.getUpdatedAt()
            )
            for group in groups
        ]
    except Exception as e:
        print(f'Error getting user groups: {e}')
        raise e

@pydantic_agent.tool
def get_debt_by_group(ctx: RunContext[MyDeps], group_id: int) ->List[GetDebtResponse]:
    """
    Get the debts of the current user in a specific group from the Splitwise client.
    This function retrieves the debts that the current user has in a specific group.

    Args:
        ctx: The context object containing the Splitwise client.
        group_id: The ID of the group to retrieve debts from.

    Returns:
        List[GetDebtResponse]: A response object containing the debts of the current user in the specified group.
    """
    debts = ctx.deps.client.get_debt_by_group(group_id)
    response = []
    for debt in debts:
        from_user = debt.getFromUser()
        to_user = debt.getToUser()
        amount = debt.getAmount()
        currency_code = debt.getCurrencyCode()
        response.extend(GetDebtResponse(owes_user_id=from_user,owed_user_id=to_user, amount=amount, currency_code=currency_code))
    return response

@pydantic_agent.tool
def get_user(ctx: RunContext[MyDeps], user_id: int) -> SplitwiseUser:
    """
    Get the splitwise user by ID.
    This function retrieves the user information from splitwise by ID.

    Args:
        ctx: The context object containing the Splitwise client.
        user_id: The ID of the user to retrieve.

    Returns:
        SplitwiseUser: The user's information.
    """
    try:
        user = ctx.deps.client.get_user(user_id)
        if user is None:
            return None
        return SplitwiseUser(
            id=user.getId(),
            first_name=user.getFirstName(),
            last_name=user.getLastName(),
            email=user.getEmail()
        )
    except Exception as e:
        print(f'Error getting user by ID: {e}')
        raise e

# def get_all_debts(self,user_id: int):
#     if not self.client:
#         raise ValueError("Client not initialized. Please login first.")
#     groups = self.get_groups()
#     res = list[GetDebtResponse]()
#     for group in groups:
#         debt=self.get_my_debt(group.id, user_id)
#         if debt:
#             res.append(debt)
#     return res