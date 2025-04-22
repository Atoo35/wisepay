
from app.db import dao as db
import json
from typing import List, Optional
from .services.ai import pydantic_agent,MyDeps
from .models.models import CurrentUser, GetDebtResponse, ListGrpResponse, PaymanBalanceInput, PaymanCryptoPayee, PaymanSearchInput, PaymanTestPayee, PaymanWalletPayee,SplitwiseUser
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
        ctx.deps.splitwise_client.set_token(token_dict)
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
        current_user = ctx.deps.splitwise_client.get_current_user()
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
        groups = ctx.deps.splitwise_client.get_groups()
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
    debts = ctx.deps.splitwise_client.get_debt_by_group(group_id)
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
        user = ctx.deps.splitwise_client.get_user(user_id)
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


@pydantic_agent.tool
def get_all_payees(ctx: RunContext[MyDeps], input: PaymanSearchInput = None) -> List[dict]:
    """
    Get payees from the Payman client.
    
    This function retrieves payees from the Payman client. If a name is provided, 
    it will filter payees by that name. If no name is provided, it will return all payees.

    Args:
        ctx: The context object containing the Payman client.
        input: An optional PaymanSearchInput object containing the name to filter payees by.

               If None, all payees will be returned.

    Returns:
        List[dict]: A list of payee objects.
    """
    try:
        payees = ctx.deps.payman_client.get_all_payees(input)
        return payees if payees else []
    except Exception as e:
        print(f'Error getting payees: {e}')
        raise e
    
@pydantic_agent.tool
def get_payman_balance(ctx: RunContext[MyDeps], input: PaymanBalanceInput) -> float:
    """
    Create a new payee using the Payman client.

    This function allows you to create either a Payman Wallet payee or a Crypto Address payee.

    Args:
        ctx: The context object containing the Payman client.
        input: A PaymanWalletPayee or PaymanCryptoPayee object containing the necessary details for creating a payee.

        type: The type of payee to create. Must be one of the following:
            - PAYMAN_WALLET: For payees identified by a wallet paytag.
            - CRYPTO_ADDRESS: For payees identified by a crypto address.
            - US_ACH: For bank account-based payees (currently unsupported in this version).

        name: The name of the payee.
        payman_wallet_paytag: Required if type is PAYMAN_WALLET.
        address: Required if type is CRYPTO_ADDRESS.
        chain: Required if type is CRYPTO_ADDRESS (e.g., Ethereum, Polygon).
        currency: Required if type is CRYPTO_ADDRESS (e.g., USDC, ETH).
        contact_details: Optional. Includes contact email, phone number, or address for the payee.
        tags: Optional. A list of string tags used to categorize or label the payee.

    Returns:
        The created payee object or an error if creation fails.
    """
    try:
        balance = ctx.deps.payman_client.get_balance(input)
        return balance if balance else 0.0
    except Exception as e:
        print(f'Error getting payman balance: {e}')
        raise e
    
@pydantic_agent.tool
def create_payman_payee(ctx: RunContext[MyDeps], input: PaymanWalletPayee | PaymanCryptoPayee | PaymanTestPayee):
    """
    Use this tool to create a new payee in Payman. You can create either a Payman Wallet payee or a Crypto Address payee.

    IMPORTANT:
    - Only use this tool after the user has clearly provided the necessary details (name, type, etc.).
    - Always set the `type` to one of: "PAYMAN_WALLET", "CRYPTO_ADDRESS", "US_ACH","TEST_RAILS".
    - For Wallet payees:
        - Required: `name`, `type="PAYMAN_WALLET"`, and `payman_wallet_paytag`.
    - For Crypto payees:
        - Required: `name`, `type="CRYPTO_ADDRESS"`, `address`, `chain`, and `currency`.
        - Optional: `contact_details` like email, phone number, or address.

    Optional:
    - `tags` can be provided as a list of strings to help categorize the payee.
    - `contact_details` should only be used for CRYPTO_ADDRESS payees.

    DO NOT use this tool if any required field is missing. Prompt the user for missing fields in a clear way.
    """

    try:
        payee = ctx.deps.payman_client.create_payee(input)
        return payee
    except Exception as e:
        print(f"Error creating payee: {e}")
        raise e
        