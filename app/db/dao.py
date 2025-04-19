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

def get_user_by_email(email: str) -> UserResponse:
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