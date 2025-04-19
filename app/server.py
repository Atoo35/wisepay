from typing import List
from fastapi import FastAPI
from app.models.models import MyDeps,ListGrpResponse,CurrentUser
# from app.services.s_client import SplitwiseUser
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .services.ai import pydantic_agent
import os
import app.tools
from app.db import dao as db
from app.services.splitwise_client import SplitwiseClientWrapper
from splitwise import Splitwise
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
        splitwise = Splitwise(os.getenv('SPLITWISE_API_KEY'), os.getenv('SPLITWISE_API_SECRET'))
        access_token = splitwise.getOAuth2AccessToken(code, os.getenv('REDIRECT_URI'))
        print(f'access_token: {access_token}')
        splitwise.setOAuth2AccessToken(access_token)
        print('access_token set')
        user = splitwise.getCurrentUser()
        id = user.getId()
        email = user.getEmail()
        # res = db.get_user_by_email(user.getEmail())
        # if res is None:
        db.create_user(email, id, access_token)
        res = db.get_user_by_email(email)
    except Exception as e:
        print(f'Error: {e}')
        return JSONResponse(content={"error": str(e)}, status_code=400)
    return {"id": id, "email": email, "spliwise_id":res.splitwise_id, "paymant_id":res.payman_id, "created_at":res.created_at, "updated_at":res.updated_at}

@app.get('/init-auth')
async def init_auth():
    try:
        splitwise = Splitwise(os.getenv('SPLITWISE_API_KEY'), os.getenv('SPLITWISE_API_SECRET'))
        # Initialize the Splitwise client with your API key and secret
        url = splitwise.getOAuth2AuthorizeURL(os.getenv('REDIRECT_URI'))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    return JSONResponse(content={"url": url})

@app.get('/{id}')
async def get_user_by_id(id: int):
    try:
        # user = db.get_user_by_id(id)
        # if user is None:
        #     return JSONResponse(content={"error": "User not found"}, status_code=404)
        # # Parse JSON string to dict
        # access_token_dict = json.loads(user.oauth_token)
        # splitwise_user = SplitwiseUser(access_token_dict)

        # usr = splitwise_user.get_current_user()
        # if usr is None:
        #     return JSONResponse(content={"error": "User not found"}, status_code=404)
        
        # response  = splitwise_user.get_groups()
       
        # if response is None:
        #     return JSONResponse(content={"error": "User not found"}, status_code=404)
        deps = MyDeps(SplitwiseClientWrapper(os.getenv('SPLITWISE_API_KEY'), os.getenv('SPLITWISE_API_SECRET')))
        response = await pydantic_agent.run("get splitwise current user groups user with id 3",deps=deps,output_type=List[ListGrpResponse])
        # for group in response.output:
        #     print(f"Group ID: {group.id}, Name: {group.name}, Updated At: {group.updated_at}")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    return {"response":response.output}

# @app.get('/{id}/debts')
# async def get_user_by_id(id: int):
#     try:
#         user = db.get_user_by_id(id)
#         if user is None:
#             return JSONResponse(content={"error": "User not found"}, status_code=404)
#         # user=UserResponse(**res)
#         # Parse JSON string to dict
#         access_token_dict = json.loads(user.oauth_token)
#         splitwise_user = SplitwiseUser(access_token_dict)
#         response = splitwise_user.get_all_debts(user.id)
#         if response is None:
#             return JSONResponse(content={"error": "User not found"}, status_code=404)
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=400)
#     return response