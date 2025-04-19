import uvicorn
import app.tools
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.server:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 