import streamlit as st
import requests

API_URL = "http://localhost:1234/chat"

st.set_page_config(page_title="Gig Worker AI", page_icon="👷")

st.title("👷 Gig Worker's Intelligent Assistant")
st.markdown("---")
st.markdown("""
**Expert AI for Gig Work**
- 🕵️ **Find Jobs**: Incoming feed analysis (Urgency, Location).
- 💰 **Smart Pricing**: Historical data analysis for accurate quotes.
- 🤝 **Worker Matching**: Find verified 'Elite' workers.
""")

# Sidebar: Coverage Info
with st.sidebar:
    st.header("📍 Coverage Area")
    st.success("City: **Bangalore**")
    
    with st.expander("Supported Areas (60+)"):
        st.markdown("""
        - **Central**: MG Road, Shivajinagar, Frazer Town
        - **North**: Hebbal, Yelahanka, RT Nagar, Malleswaram
        - **South**: Jayanagar, BTM Layout, Koramangala, HSR Layout, JP Nagar, Electronic City
        - **East**: Indiranagar, Whitefield, Marathahalli, Bellandur, KR Puram
        - **West**: Rajajinagar, Vijayanagar, Peenya, RR Nagar
        """)
        
    st.header("🛠️ Job Categories")
    st.markdown("""
    1. **Plumber** 🚿
    2. **Electrician** 💡
    3. **Carpenter** 🪑
    4. **AC Repair** ❄️
    5. **Maid Services** 🧹
    6. **Painter** 🎨
    7. **Civil Works** 🧱
    """)
    st.info("Product: **GigGuardian AI** v1.0")

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
