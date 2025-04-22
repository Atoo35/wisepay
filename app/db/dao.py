from pydantic_ai import RunContext
from app.db.connection import get_connection
from app.db.schemas import UserResponse, UserUpsert
from app.services.ai import pydantic_agent,MyDeps

@pydantic_agent.tool
def get_user_by_splitwise_id(ctx: RunContext[MyDeps], splitwise_id: int) -> UserResponse:
    conn = ctx.deps.db_client
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE splitwise_id = %s", (splitwise_id,))
        row = cursor.fetchone()
        if not row:
            return None
        columns = [desc[0] for desc in cursor.description]
        return UserResponse(**dict(zip(columns, row)))
    finally:
        conn.close()

    
@pydantic_agent.tool_plain
def get_user_by_id(id: int) -> UserResponse:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        row = cursor.fetchone()
        if not row:
            return None
        columns = [desc[0] for desc in cursor.description]
        print(row)
        return UserResponse(**dict(zip(columns, row)))
    finally:
        cursor.close()

@pydantic_agent.tool
def get_user_by_email(ctx: RunContext[MyDeps],email: str) -> UserResponse:
    """
    Get user by email.
    This function retrieves a user from the database using their email address.

    It returns a UserResponse object containing the user's information.

    If the user is not found, it returns None.

    Args:
        email (str): The email address of the user to retrieve.
    
    Returns:
        UserResponse: The user information if found, otherwise None.
    """
    conn = ctx.deps.db_client
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        row =  cursor.fetchone()
        if not row:
            return None
        columns = [desc[0] for desc in cursor.description]
        return UserResponse(**dict(zip(columns, row)))
    finally:
        cursor.close()

@pydantic_agent.tool_plain
def upsert_user(user: UserUpsert):
    """
    This function is used to upsert the user in the database.
    Make sure to check if the user exists prior to setting values for this function since we dont want to overwrite the data which isnt being filled.
    For example: It's likely that you would only update payman id at a given time and not splitwise id, here we risk loosing splitwise id if we dont send the current data.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (email, splitwise_id, oauth_token,payman_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE
            SET splitwise_id = EXCLUDED.splitwise_id,
                oauth_token = EXCLUDED.oauth_token,
                payman_id = EXCLUDED.payman_id,
                updated_at = NOW();
        """, (user.email, user.splitwise_id, user.oauth_token,user.payman_id))
        conn.commit()
    finally:
        cursor.close()

