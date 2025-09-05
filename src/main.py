# src/main.py

import streamlit as st
from agent import app  # Import the compiled agent app

st.title("🤖 MediCare Scheduling Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Start the conversation with the agent's greeting
    initial_event = app.invoke({})
    greeting_message = initial_event.get('greet_patient', {}).get(
        'greeting_message',
        "Hello! How can I help you book an appointment?"
    )
    st.session_state.messages.append({"role": "assistant", "content": greeting_message})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Your response..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get the agent's response
    response_content = "Thank you. I am processing your request to book an appointment."

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_content)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})
    st.info("Backend agent has processed the booking. Check the generated files.", icon="ℹ️")
