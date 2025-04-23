from typing import List
from fastapi import FastAPI
from app.db.connection import get_connection
from app.db.schemas import UserUpsert
from app.models.models import ListGrpResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.services.paymanai_client import PaymanWrapper
from .services.ai import pydantic_agent,MyDeps
import os
import app.tools as tools
from app.db import dao as db
from app.services.splitwise_client import SplitwiseClientWrapper
from splitwise import Splitwise
from .config import settings
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
        splitwise = Splitwise(settings.SPLITWISE_API_KEY, settings.SPLITWISE_API_SECRET)
        access_token = splitwise.getOAuth2AccessToken(code, settings.REDIRECT_URI)
        print(f'access_token: {access_token}')
        splitwise.setOAuth2AccessToken(access_token)
        print('access_token set')
        user = splitwise.getCurrentUser()
        id = user.getId()
        email = user.getEmail()
        # res = db.get_user_by_email(user.getEmail())
        # if res is None:
        db.upsert_user(UserUpsert(email=email,splitwise_id=id,oauth_token=access_token))
        res = db.get_user_by_email(email)
    except Exception as e:
        print(f'Error: {e}')
        return JSONResponse(content={"error": str(e)}, status_code=400)
    return {"id": id, "email": email, "spliwise_id":res.splitwise_id, "paymant_id":res.payman_id, "created_at":res.created_at, "updated_at":res.updated_at}

@app.get('/init-auth')
async def init_auth():
    try:
        splitwise = Splitwise(settings.SPLITWISE_API_KEY, settings.SPLITWISE_API_SECRET)
        # Initialize the Splitwise client with your API key and secret
        url = splitwise.getOAuth2AuthorizeURL(settings.REDIRECT_URI)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    return JSONResponse(content={"url": url})

@app.get('/{id}')
def get_user_by_id(id: int):
    try:
        deps = MyDeps(
            splitwise_client=SplitwiseClientWrapper(settings.SPLITWISE_API_KEY, settings.SPLITWISE_API_SECRET),
            payman_client=PaymanWrapper(),
            db_client=get_connection()
        )
        response =  pydantic_agent.run_sync(f"get splitwise current user groups user with id {id}",deps=deps,output_type=List[ListGrpResponse])
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