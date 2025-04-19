from fastapi import FastAPI
from app.db.schemas import ListGrpResponse, UserResponse
from app.services.s_client import SplitwiseUser
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db import dao as db
import json

# api_router = APIRouter()
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/authorize/callback")
async def authorize(code: str = None):
    try:
        splitwise = SplitwiseUser()
        access_token = splitwise.fetch_access_token(code)
        splitwise.set_access_token(access_token)
        user = splitwise.get_current_user()
        res = db.get_user_by_email(user['email'])
        if res is None:
            db.create_user(user['email'], user['id'], access_token)
            res = db.get_user_by_email(user['email'])
        print(f'res: {res}')
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    return JSONResponse(content=user, status_code=200)

@app.get('/init-auth')
async def init_auth():
    try:
        splitwise = SplitwiseUser()
        # Initialize the Splitwise client with your API key and secret
        url = splitwise.init_auth()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    return JSONResponse(content={"url": url})

@app.get('/{id}')
async def get_user_by_id(id: int):
    try:
        user = db.get_user_by_id(id)
        if user is None:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        # Parse JSON string to dict
        access_token_dict = json.loads(user.oauth_token)
        splitwise_user = SplitwiseUser(access_token_dict)

        usr = splitwise_user.get_current_user()
        if usr is None:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        response  = splitwise_user.get_groups()
       
        if response is None:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    return {"user":usr,"response":response}

@app.get('/{id}/debts')
async def get_user_by_id(id: int):
    try:
        user = db.get_user_by_id(id)
        if user is None:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        # user=UserResponse(**res)
        # Parse JSON string to dict
        access_token_dict = json.loads(user.oauth_token)
        splitwise_user = SplitwiseUser(access_token_dict)
        response = splitwise_user.get_all_debts(user.id)
        if response is None:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    return response