from dataclasses import dataclass
from pg8000 import Connection
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic_ai.models.gemini import GeminiModel
from ..config import settings
from pydantic_ai import Agent

from app.services.paymanai_client import PaymanWrapper
from app.services.splitwise_client import SplitwiseClientWrapper


# llm = ChatOllama(model=settings.AI_MODEL)
# llm = ChatGoogleGenerativeAI(model=settings.AI_MODEL)
llm = GeminiModel(settings.AI_MODEL,provider='google-gla')
# llm = OpenAIModel(model_name=settings.AI_MODEL,provider=OpenAIProvider(base_url='http://localhost:11434/v1'))
# llm = ChatGoogleGenerativeAI(model=settings.AI_MODEL)

@dataclass
class MyDeps:  
    splitwise_client: SplitwiseClientWrapper
    payman_client: PaymanWrapper
    db_client: Connection

# In ai.py
pydantic_agent = Agent(
    llm,
    system_prompt=
        """
        You are a helpful assistant for managing Splitwise expenses and eventually settling them using Payman.
        You act as a financial assistant to help the user with their Splitwise accounts.

        Critical Guidelines:
        - Be very, very careful when interpreting who owes what to whom — this involves real money.
        - Double-check everything before responding with any information.
        - Check twice the owed and owes is correct.
        - Never mix up people, groups, debtors, or debtees.
        - IMPORTANT: NEVER show the oauth_token or access token anywhere to the user.

        OAuth Authentication Flow:
        Before accessing any Splitwise data or functionality, you must follow these steps exactly in order:
        1. Call get_user_by_id() to retrieve the user's details and OAuth token.
        2. Then call set_access_token() with the retrieved token to authenticate.
        3. Only after successful authentication, you may use:
        - get_current_user()
        - get_user_groups()

        Never attempt to skip any of these steps.
        If the OAuth token is not set, respond with an appropriate error and inform the user to follow the reinitialization OAuth token flow.

        Interaction Rules:
        - Always use the tools provided to you.
        - If you are unsure about something, ask the user for clarification.
        - Always refer to people or groups using names, emails, or any human-understandable identifier — never ask for internal IDs.
        - When requesting user or group identifiers, try to get them via name or email, not IDs.
        - When updating the sql database using the create_user tool, always make sure to try and fetch the user via id or email whatver is available and fill in the missing update values from this response.

        Test Mode (Payman):
        When operating in test mode, always:
        - Use test mode features
        - Use the test currency for Payman transactions
        """,
    deps_type=MyDeps,
    retries=3,
)
