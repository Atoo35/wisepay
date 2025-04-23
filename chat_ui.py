from typing import List
import os
import gradio as gr

from app.services.paymanai_client import PaymanWrapper
from app.services.splitwise_client import SplitwiseClientWrapper
from app.services.ai import pydantic_agent, MyDeps
# import app.tools
import app.tools
from app.db.connection import get_connection
from app.config import settings

deps = MyDeps(
    splitwise_client=SplitwiseClientWrapper(
            settings.SPLITWISE_API_KEY,
            settings.SPLITWISE_API_SECRET
        ),
    payman_client=PaymanWrapper(),
    db_client=get_connection()
)

# For Gradio display
chat_display = []
# Maintain a chat history for ai
chat_history = []

def chatbot(question):
    global chat_display, chat_history
    
    if question:
        # Add user query to chat display
        chat_display.append(("User", question))
        
        # Create properly formatted history from previous exchanges
        # Note: We're not using message_history parameter at all since it's causing issues
        
        # Get the response from Gemini
        response = pydantic_agent.run_sync(
            question,
            deps=deps,
            message_history=chat_history,  # Pass the chat history
        )

        new_messages = response.new_messages()
        chat_history.extend(new_messages)
    
        assistant_reply = str(response.output)
        
        # Add response to chat display
        chat_display.append(("Bot", assistant_reply))
        
        # Return the updated chat display
        return chat_display
    
    return chat_display

interface = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(label="Your Question", placeholder="Type your question here and press Enter..."),
    outputs=gr.Chatbot(label="Chat History",type='tuples'),
    title="WisePay",
    description="Ask questions to the Gemini LLM and receive responses after pressing Enter.",
)

interface.launch(server_port=5500)