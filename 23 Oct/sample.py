import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import streamlit as st

# 1. Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# 2. Initialize LangChain model pointing to OpenRouter
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct:free",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

st.title("AI Assistant")

user_input = st.text_area("Enter your message:")

if st.button("Send"):
    if not user_input.strip():
        st.error("Please enter a message.")
    else:
        try:
            llm = ChatOpenAI(
                model="mistralai/mistral-7b-instruct",
                temperature=0.7,
                max_tokens=256,
                api_key=api_key,
                base_url=base_url,
            )

            messages = [
                SystemMessage(content="You are a helpful and concise AI assistant."),
                HumanMessage(content=user_input)
            ]

            with st.spinner("Generating response..."):
                response = llm.invoke(messages)

            st.subheader("Response:")
            st.write(response.content.strip() if response.content else "(no response)")

        except Exception as e:
            st.error(f"Error: {e}")

# messages = [
#     SystemMessage(content="You are a helpful and concise AI assistant."),
#     HumanMessage(content="<s>[INST] Explain in simple terms how convolutional neural networks work. [/INST]"),
# ]