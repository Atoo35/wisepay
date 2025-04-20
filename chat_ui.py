import os
from typing import List
import streamlit as st
from dotenv import load_dotenv

from app.models.models import ListGrpResponse, MyDeps
from app.services.splitwise_client import SplitwiseClientWrapper
from app.services.ai import pydantic_agent
import app.tools
from app.db import dao as db

# Load environment variables from .env
load_dotenv()

st.title("WisePay")
deps = MyDeps(SplitwiseClientWrapper(
            os.getenv('SPLITWISE_API_KEY'),
            os.getenv('SPLITWISE_API_SECRET')
        ))

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new prompt
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                    if m["role"] in {"user", "assistant"}
                ]
        # You can uncomment output_type if you want structured output
        response = pydantic_agent.run_sync(
            prompt,
            deps=deps,
            history=history,
            # message_history=history,
            # output_type=List[ListGrpResponse]
        )

        assistant_reply = str(response.output)  # Or format however you want
        st.markdown(assistant_reply)

    # Save assistant message properly
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
