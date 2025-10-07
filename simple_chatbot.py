import json
import random
import requests
import streamlit as st
from openai import AzureOpenAI

with st.sidebar:
    openai_api_key = st.text_input("Azure OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an Azure OpenAI API key](https://itsc.hkust.edu.hk/services/it-infrastructure/azure-openai-api-service)"

model_name = "gpt-4o-mini"

st.title("💬 Healthcare Chatbot")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your Azure OpenAI API key to continue.")
        st.stop()

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    st.chat_message("user").write(prompt)

    # setting up the OpenAI model
    client = AzureOpenAI(
        api_key=openai_api_key,
        api_version="2025-02-01-preview",
        azure_endpoint="https://hkust.azure-api.net/",
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=st.session_state.messages
    )

    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)