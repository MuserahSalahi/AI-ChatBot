import os
import json
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

#  MULTIPLE API KEYS FALLBACK LIST
# SECURE MULTIPLE API KEYS LOAD FROM .env
raw_keys = os.getenv("GROQ_API_KEYS", "")
GROQ_API_KEYS = [key.strip() for key in raw_keys.split(",") if key.strip()]

# Backup check: if .env is empty or file is missing
if not GROQ_API_KEYS:
    st.error(" Error: API_KEYS not found in .env file! Please check your environment configuration.")
    st.stop()


# track of which key is being used
if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

# 1. Page Configuration Setup
st.set_page_config(page_title="AI Chatbot", layout="wide")

STORAGE_FILE = "chat_sessions.json"

def load_all_sessions():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_all_sessions(sessions):
    with open(STORAGE_FILE, "w") as f:
        json.dump(sessions, f, indent=4)

# Premium UI CSS
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); }
    .main-title { text-align: center; font-family: 'Inter', sans-serif; font-weight: 800; color: #1e293b; margin-top: -30px; margin-bottom: 30px; font-size: 2.8rem; }
    .main-sticky-footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #ffffff; border-top: 2px solid #cbd5e1; color: #0f172a; text-align: center; padding: 12px 0; font-size: 14px; font-weight: 700; z-index: 999999; box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.05); }
    .main .block-container { padding-bottom: 110px !important; max-width: 900px; }
    .stChatMessage { background-color: #ffffff !important; border-radius: 16px !important; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03) !important; margin-bottom: 16px !important; padding: 20px !important; border: 1px solid #e2e8f0 !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e2e8f0; }
    </style>
    """,
    unsafe_allow_html=True,
)

all_sessions = load_all_sessions()

if "active_session_id" not in st.session_state:
    if all_sessions:
        st.session_state.active_session_id = list(all_sessions.keys())[-1]
    else:
        st.session_state.active_session_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if "chat_history" not in st.session_state:
    if st.session_state.active_session_id in all_sessions:
        st.session_state.chat_history = all_sessions[st.session_state.active_session_id]
    else:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your Smart AI Assistant. How can I help you today?"}
        ]

# Sidebar
with st.sidebar:
    st.markdown("###  Chat Controller")
    if st.button("➕ Start New Conversation", use_container_width=True):
        new_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.active_session_id = new_id
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your Smart AI Assistant. How can I help you today?"}
        ]
        st.rerun()
        
    st.markdown("---")
    st.markdown("###  Conversation History Logs")
    if all_sessions:
        for session_id in reversed(list(all_sessions.keys())):
            preview_text = all_sessions[session_id][1]["content"][:22] + "..." if len(all_sessions[session_id]) > 1 else session_id
            button_label = f"💬 {preview_text}"
            if session_id == st.session_state.active_session_id:
                button_label = f"📌 {preview_text} (Active)"
                
            if st.button(button_label, key=session_id, use_container_width=True):
                st.session_state.active_session_id = session_id
                st.session_state.chat_history = all_sessions[session_id]
                st.rerun()

st.markdown("<h1 class='main-title'> AI Chatbot</h1>", unsafe_allow_html=True)

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

st.markdown('<div class="main-sticky-footer">AI ChatBot Created by Muserah Salahi</div>', unsafe_allow_html=True)

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful, brilliant, and professional AI assistant. Provide accurate textual responses."),
        ("placeholder", "{chat_history}"),
        ("user", "{question}"),
    ]
)
output_parser = StrOutputParser()

#  FUNCTION TO INITIALIZE CHAIN WITH FALLBACK LOGIC
def invoke_llm_with_fallback(question, formatted_history):
    """Tries primary model/key, falls back to backup model or next key if rate limit hits."""
    models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    
    start_key_idx = st.session_state.current_key_index
    total_keys = len(GROQ_API_KEYS)
    
    # Loop through available API keys
    for key_offset in range(total_keys):
        current_idx = (start_key_idx + key_offset) % total_keys
        active_key = GROQ_API_KEYS[current_idx]
        
        # Loop through both models for the current active key
        for model_name in models_to_try:
            try:
                # Initialize LLM with selected key and model
                llm = ChatGroq(model=model_name, groq_api_key=active_key)
                chain = prompt | llm | output_parser
                
                # Execute pipeline
                response = chain.invoke({
                    "question": question,
                    "chat_history": formatted_history
                })
                
                # if success , update session state key index to avoid future lags
                st.session_state.current_key_index = current_idx
                return response, model_name
                
            except Exception as e:
                error_msg = str(e).lower()
                # Check if it's a rate limit or exhaustion error
                if "rate_limit" in error_msg or "429" in error_msg or "limit" in error_msg:
                    # Silently proceed to next model or next API Key loop
                    continue
                else:
                    # if any other error occurs, raise it
                    raise e
                    
    # If all keys and models are exhausted
    raise Exception("API Keys or free limits have been exhausted for the current window.")

# Chat input handler
if user_query := st.chat_input("Type your question here..."):
    
    with st.chat_message("user"):
        st.write(user_query)
        
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        with st.spinner("Processing Response via Smart Pipeline..."):
            try:
                formatted_history = []
                for msg in st.session_state.chat_history[:-1]:
                    role = "human" if msg["role"] == "user" else "assistant"
                    formatted_history.append((role, msg["content"]))
                
                # Invoke utilizing fallback architecture
                response, used_model = invoke_llm_with_fallback(user_query, formatted_history)
                
                st.write(response)
                # Small badge showing which model handled the load
                st.caption(f"Processed via node: `{used_model}`")
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                all_sessions[st.session_state.active_session_id] = st.session_state.chat_history
                save_all_sessions(all_sessions)
                st.rerun()
                
            except Exception as e:
                st.error(f"Fallback Engine Failure: {e}")