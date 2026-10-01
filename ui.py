import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

EXAMPLES = [
    "What databases has he worked with?",
    "Has he used AWS Glue?",
    "Tell me about the HRMS project",
    "What is his education?",
]

st.set_page_config(page_title="HashAi")
st.title("HashAi")
st.caption("Ask anything about Harsh Saliya. Answers come from his resume only.")

if "history" not in st.session_state:
    st.session_state.history = []


def fetch_answer(question):
    try:
        res = requests.post(f"{API_URL}/ask", json={"question": question}, timeout=60)
        res.raise_for_status()
        return res.json()["answer"]
    except requests.exceptions.ConnectionError:
        return f"Could not reach the API at {API_URL}. Is it running?"
    except requests.exceptions.Timeout:
        return "The API took too long to respond."
    except Exception as err:
        return f"Something went wrong: {err}"


with st.sidebar:
    st.subheader("Try asking")
    for example in EXAMPLES:
        if st.button(example, use_container_width=True):
            st.session_state.pending = example

    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.history = []
        st.rerun()

for question, answer in st.session_state.history:
    st.chat_message("user").write(question)
    st.chat_message("assistant").write(answer)

question = st.chat_input("What would you like to know?")
if not question:
    question = st.session_state.pop("pending", None)

if question:
    st.chat_message("user").write(question)
    with st.chat_message("assistant"):
        with st.spinner("Looking through the resume..."):
            answer = fetch_answer(question)
        st.write(answer)
    st.session_state.history.append((question, answer))
