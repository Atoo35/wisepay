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

pydantic_agent = Agent(
    llm,
    system_prompt=(
        "You are a helpful assistant, you have access to all the tools. "
        "Don't hallucinate, if you don't know the answer say 'I don't know'. "
        "Don't make up any information, if you don't know the answer say 'I don't know'. "
        "To use any splitwise tool method this is the process: "
        "1. Use the db to get the user by id. "
        "2. Use the oauth token obtained to set the access token for the splitwise client. "
        "3. Now you can use the splitwise tools as needed."
    ),
    deps_type=MyDeps
)
