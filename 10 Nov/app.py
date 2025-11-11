import streamlit as st
import requests

st.set_page_config(page_title="FastAPI + Streamlit Demo", layout="centered")

st.title("🧩 FastAPI + Streamlit Integration")

st.markdown("""
**Examples:**
- `Add 45 and 35`
- `Tell me todays date`
- `Reverse this Word: Sample`
""")

user_input = st.text_input("Enter your query:")
if st.button("Submit"):
    if user_input:
        response = requests.post(
            "http://127.0.0.1:8000/process/",
            json={"text": user_input}
        )
        if response.status_code == 200:
            st.success(response.json()["answer"])
        else:
            st.error("Error: Unable to connect to FastAPI backend")
