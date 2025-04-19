
import os
import asyncio
from typing import List
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os
from pydantic_ai import Agent
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
# from app.services.ai import MyDeps,
from app.services.ai import pydantic_agent
from app.models.models import ListGrpResponse, MyDeps
import app.tools
# from splitwise import Splitwise
from app.models.models import SplitwiseClientWrapper

load_dotenv(override=True)


@pydantic_agent.tool_plain
def multiply(a: int, b:int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a+b

@pydantic_agent.tool_plain  
def roll_die() -> str:
    """Roll a six-sided die and return the result."""
    return str(2)

deps = MyDeps(SplitwiseClientWrapper(os.getenv('SPLITWISE_API_KEY'), os.getenv('SPLITWISE_API_SECRET')))
response = pydantic_agent.run_sync("get splitwise current user groups user with id 3",deps=deps,output_type=List[ListGrpResponse])
for group in response.output:
    print(f"Group ID: {group.id}, Name: {group.name}, Updated At: {group.updated_at}")

# print(response.tool_calls)