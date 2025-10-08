import json
import streamlit as st
from openai import APIConnectionError, APIStatusError
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
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=st.session_state.messages
        )
    except APIConnectionError as err:
        error_msg = "I couldn't reach Azure OpenAI. Please check your connection and try again."
        st.error(str(err))
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        st.chat_message("assistant").write(error_msg)
        st.stop()
    except APIStatusError as err:
        error_msg = "Azure OpenAI returned an error. Please verify your credentials and try again."
        st.error(str(err))
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        st.chat_message("assistant").write(error_msg)
        st.stop()
    except Exception as err:  # noqa: BLE001
        error_msg = "Something went wrong while contacting Azure OpenAI. Please try again later."
        st.error(str(err))
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        st.chat_message("assistant").write(error_msg)
        st.stop()

    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
