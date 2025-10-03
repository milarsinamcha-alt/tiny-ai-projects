import os
import streamlit as st
from google import genai
from google.genai import types

# --- 1. CONFIGURATION AND INITIALIZATION ---

# Set Streamlit page details
st.set_page_config(
    page_title="Tiny AI Q&A Bot",
    page_icon="🤖",
    layout="centered"
)

# Use st.cache_resource to initialize the Gemini client only once.
# This prevents unnecessary re-initialization on every user interaction (Streamlit rerun).
@st.cache_resource
def initialize_gemini_client():
    """Initializes and returns the Gemini client."""
    
    # Check if GEMINI_API_KEY is available in the environment variables (Hugging Face Secret)
    if 'GEMINI_API_KEY' not in os.environ:
        st.error(
            "API Key not found. Please add your GEMINI_API_KEY "
            "as a secret in your Hugging Face Space settings."
        )
        return None # Return None if initialization fails
        
    try:
        # Client initialization will automatically use the GEMINI_API_KEY from os.environ
        client = genai.Client()
        return client
    except Exception as e:
        st.error(f"Error initializing Gemini client: {e}")
        return None

# Get the client instance
gemini_client = initialize_gemini_client()

# --- 2. API CALL FUNCTION ---

def get_gemini_response(client, user_question):
    """
    Sends a single user question to the Gemini API and returns the text response.
    The system instruction is integrated into the prompt for concise context.
    """
    if not client:
        return "The Gemini client failed to initialize. Please check API key setup."
        
    # Define the system instructions/prompt structure
    system_instruction = (
        "You are a helpful, brief, and concise Q&A assistant for an internship. "
        "Respond directly to the user's question without unnecessary pleasantries."
    )
    
    # Structure the chat history and new message for the API call
    # Note: For simplicity in this non-chat-history Q&A, we pass the user_question
    # directly as the content part, along with the system instruction.
    # For conversational history, you would format a list of types.Content objects.
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            # Pass the user question as a content part
            contents=[types.Content(role="user", parts=[types.Part.from_text(user_question)])],
            # Pass the system instruction for model guidance
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        
        return response.text
        
    except Exception as e:
        return f"An API error occurred: {e}" 

# --- 3. STREAMLIT UI AND INTERACTION LOOP ---

st.header("✨ Your Streamlit-Powered AI Q&A Bot")
st.markdown("Ask any question and the Gemini model will provide a concise answer.")

# Initialize chat history in Streamlit's session state
# This is crucial for Streamlit to remember the conversation between reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []
    if gemini_client:
        # Add an initial greeting message from the bot
        st.session_state.messages.append(
            {"role": "assistant", "content": "Hello! I'm ready to answer your questions. Ask away!"}
        )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input via the chat input box
if prompt := st.chat_input("Enter your question here..."):
    
    # 1. Add user message to session state and display it immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get the bot's response
    # Use st.spinner to show a loading indicator while the API call is running
    with st.spinner("Thinking..."):
        bot_response = get_gemini_response(gemini_client, prompt)

    # 3. Display the bot's response
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # 4. Add bot response to session state
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
