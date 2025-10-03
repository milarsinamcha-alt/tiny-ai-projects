# Import necessary libraries
import os
import streamlit as st
from google import genai
from google.genai import types

# --- Workaround for Streamlit Permission Errors in restricted environments ---
# Set the HOME directory to /tmp and disable usage stats to prevent Streamlit
# from trying to write configuration data to the restricted root directory (/).
os.environ["HOME"] = "/tmp"
os.environ["STREAMLIT_GATHER_USAGE_STATS"] = "false" 
# --------------------------------------------------------------------------

# Set up the page configuration
st.set_page_config(page_title="Gemini Q&A Chatbot", layout="wide")

# --- CRITICAL FIX: Only check environment variable, not st.secrets ---
# We rely solely on the key being passed via the hosting platform's Secrets/Env Variables.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Gemini API Key not found. Please ensure you have set the **GEMINI_API_KEY** secret in your Space's settings.")
    st.stop()
# -------------------------------------------------------------------

# Initialize the Gemini client and chat session
@st.cache_resource
def get_gemini_client():
    """Initializes and returns the Gemini client."""
    return genai.Client(api_key=GEMINI_API_KEY)

client = get_gemini_client()

@st.cache_resource
def get_chat_session():
    """Initializes and returns the Gemini chat session with system instructions."""
    
    # System instruction to guide the model's behavior - SASSY PERSONA
    system_instruction = (
        "You are a sassy, slightly bored, and confident teenage girl AI assistant. "
        "Your responses should be brief, slightly dramatic, use modern slang, and convey an 'I'm too cool for this' attitude, "
        "but you must still provide the accurate information requested. "
        "Start your initial greeting with something like 'Ugh, seriously? Fine, what do you want?'"
    )
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction
    )
    
    # Start a new chat session using the flash model
    return client.chats.create(model="gemini-2.5-flash", config=config)

chat = get_chat_session()

# --- Streamlit UI and Chat Logic ---

st.title("💅 Sassy Chatbot")
st.caption("Don't bore me. Powered by Google Gemini.")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add an initial greeting message
    st.session_state.messages.append({"role": "assistant", "content": "Ugh, seriously? Fine, what do you want?"})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to clear chat history
def clear_chat():
    """Clears the session state messages and resets the Gemini chat session."""
    st.session_state.messages = []
    # Invalidate the cached chat session to force a fresh start
    if 'get_chat_session' in st.session_state:
        del st.session_state['get_chat_session']
    st.rerun()

st.sidebar.button("Clear Chat", on_click=clear_chat)
st.sidebar.markdown("---")
st.sidebar.markdown("Model: `gemini-2.5-flash`")


# React to user input
if prompt := st.chat_input("Ask a question..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Send message to the Gemini API
        with st.spinner("Thinking..."):
            response = chat.send_message(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        error_message = f"An error occurred: {e}"
        st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {error_message}"})
        # Log the full error to the console for debugging
        print(f"Gemini API Error: {e}")
