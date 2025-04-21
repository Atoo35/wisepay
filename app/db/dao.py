from app.db.connection import get_connection
from app.db.schemas import UserResponse
from app.services.ai import pydantic_agent

def get_user_by_splitwise_id(splitwise_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # cursor.execute("SELECT * FROM users WHERE splitwise_id = %s", (splitwise_id,))
        cursor.execute("SELECT * FROM users;")
        return cursor.fetchall()
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
        return UserResponse(**dict(zip(columns, row)))
    finally:
        conn.close()

@pydantic_agent.tool_plain
def get_user_by_email(email: str) -> UserResponse:
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
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        row =  cursor.fetchone()
        if not row:
            return None
        columns = [desc[0] for desc in cursor.description]
        return UserResponse(**dict(zip(columns, row)))
    finally:
        conn.close()

@pydantic_agent.tool_plain
def create_user(email:str,splitwise_id: int, oauth_token: str):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (email, splitwise_id, oauth_token)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO UPDATE
            SET splitwise_id = EXCLUDED.splitwise_id,
                oauth_token = EXCLUDED.oauth_token,
                updated_at = NOW();
        """, (email, splitwise_id, oauth_token))
        conn.commit()
    finally:
        conn.close()