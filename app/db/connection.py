import pg8000
from ..config import settings


DB_HOST = settings.DB_HOST
DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_PORT = settings.DB_PORT

def get_connection():
    try:
        conn = pg8000.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print("❌ Failed to connect to DB:", e)
        raise
