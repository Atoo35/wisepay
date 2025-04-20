from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic_ai.models.gemini import GeminiModel
import os
from pydantic_ai import Agent
from ..models.models import MyDeps

load_dotenv(override=True)

# llm = ChatOllama(model=os.getenv('MODEL'))
# llm = ChatGoogleGenerativeAI(model=os.getenv('MODEL'))
llm = GeminiModel(os.getenv('MODEL'),provider='google-gla')
# llm = OpenAIModel(model_name=os.getenv('MODEL'),provider=OpenAIProvider(base_url='http://localhost:11434/v1'))
# llm = ChatGoogleGenerativeAI(model=os.getenv('MODEL'))

# input = [
#     ("human","hi how are you")
# ]

# In ai.py
pydantic_agent = Agent(
    llm,
    system_prompt=(
        "You are a helpful assistant for managing Splitwise expenses. "
        "IMPORTANT: To use any Splitwise functionality, you MUST follow these exact steps in order:\n"
        "1. First call get_user_by_id() to retrieve the user's details and OAuth token\n"
        "2. Then call set_access_token() with the OAuth token to authenticate\n" 
        "3. Only after authentication, you can use get_current_user() or get_user_groups()\n\n"
        "Never attempt to skip steps or use Splitwise tools before authentication is complete.\n"
        "If the user asks about Splitwise data, always perform these authentication steps first."
    ),
    deps_type=MyDeps
)
