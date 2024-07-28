# src/main.py
import streamlit as st
from chatbot.chatbot import process_message
from utils.query_vector_store import query_vector_store
from collections import Counter
from langchain import hub
from langchain_openai import ChatOpenAI

# Load prompt and LLM
prompt = hub.pull("hwchase17/openai-tools-agent")
llm = ChatOpenAI(temperature=0, model_name='gpt-4')

# Initialize chat history with the welcome message
chat_history = [("System", "Hello! Welcome to the HR Grievance Chatbot. May I have your name, please?")]
context = ""
grievance_stage = 1  # Set initial stage to 1 since we're asking for the name

st.title("HR Pro Bot")

# Streamlit chat components
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = chat_history

if 'context' not in st.session_state:
    st.session_state.context = context

if 'grievance_stage' not in st.session_state:
    st.session_state.grievance_stage = grievance_stage

def submit_message():
    user_input = st.session_state.input_message
    if user_input:
        # Add the user input to the chat history
        st.session_state.chat_history.append(("User", user_input))
        
        response, updated_history, updated_context, updated_stage, final_response = process_message(
            user_input, st.session_state.chat_history, st.session_state.context, st.session_state.grievance_stage, llm, prompt)
        
        st.session_state.chat_history = updated_history
        st.session_state.context = updated_context
        st.session_state.grievance_stage = updated_stage

        if updated_stage == 0:
            st.session_state.admin_display = st.markdown(final_response)
        
        st.session_state.input_message = ""

# Display chat history
for i, (sender, message) in enumerate(st.session_state.chat_history):
    if sender == "System":
        if i == 0:
            st.chat_message("🎉").write(message)  # Different icon for the welcome message
        else:
            st.chat_message("💬").write(message)
    else:
        st.chat_message("💬").write(message)

# Input box for user message (fixed at the bottom)
st.text_input("Enter your message", key="input_message", on_change=submit_message)

# Set rate limit
rate_limit = 60  # Adjust this based on your estimated Gemini rate limit (requests per minute)
api_calls_counter = Counter()  # Initialize counter
