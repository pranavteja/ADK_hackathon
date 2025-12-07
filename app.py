import streamlit as st
import requests

API_URL = "http://localhost:8080/chat"

st.set_page_config(page_title="Gig Worker AI", page_icon="👷")

st.title("👷 Gig Worker's Intelligent Assistant")
st.markdown("---")
st.markdown("""
**Expert AI for Gig Work**
- 🕵️ **Find Jobs**: Incoming feed analysis (Urgency, Location).
- 💰 **Smart Pricing**: Historical data analysis for accurate quotes.
- 🤝 **Worker Matching**: Find verified 'Elite' workers.
""")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask me anything (e.g., 'Find plumber jobs in Indiranagar' or 'How much for a fan install?')"):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"text": prompt})
                if response.status_code == 200:
                    answer = response.json()["response"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")
