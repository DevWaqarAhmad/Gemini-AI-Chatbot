import streamlit as st
import requests
import time

# Flask backend URL
FLASK_API_URL = "http://127.0.0.1:5000/get_response"  # Update if deploying

st.title("Butt Karahi Chatbot 🍲")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to stream response
def response_generator(prompt):
    try:
        response = requests.post(FLASK_API_URL, json={"prompt": prompt})
        if response.status_code == 200:
            response_text = response.json().get("response", "")
            for word in response_text.split():
                yield word + " "
                time.sleep(0.05)
            return response_text  # Return full response for history
        else:
            return "❌ Error: Unable to fetch response from backend."
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"

# User Input
if prompt := st.chat_input("Ask me about Butt Karahi..."):
    # Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        response_text = st.write_stream(response_generator(prompt))
    
    # Store assistant response in chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
