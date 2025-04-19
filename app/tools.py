import json
from typing import List
from .db.dao import get_user_by_id
from .services.ai import pydantic_agent
from .models.models import CurrentUser, ListGrpResponse, MyDeps
from pydantic_ai import RunContext

@pydantic_agent.tool
def set_access_token(ctx: RunContext[MyDeps], oauth_token: str) -> None:
    """
    Set the access token for the Splitwise client.
    This function is used to authenticate the user and allow them to access their Splitwise account.

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