from google import genai
import streamlit as st
from openai import OpenAI

# Initialize the client for Gemini
gemini_client = genai.Client(api_key="AIzaSyDow4japDIMKQyM3hYwPZHxYL83XS_6hVM")

# Initialize the client for DeepSeek
deepseek_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# Streamlit app title
st.title("Chat with AI Models")
st.write("This is a simple chat app powered by Google Gemini and DeepSeek APIs. Type 'quit' to exit.")

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("### AI Models")
selected_model = st.sidebar.radio(
    "Choose an AI Model",
    ["Gemini", "DeepSeek"]  # Added DeepSeek as an option
)

# Model selection dropdown for Gemini
if selected_model == "Gemini":
    models = [
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.0-pro-exp-02-05",
        "gemini-2.0-flash-thinking-exp-01-21",
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ]
    selected_gemini_model = st.selectbox("Select a Gemini Model", models)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Enter a Prompt:")

if user_input:
    # Check if the user wants to quit
    if user_input.lower() in ["quit", "exit", "close"]:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": "Exiting the program..."})
        st.rerun()  # Refresh the UI to show the exit message
    else:
        # Add user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Generate a response based on the selected model
        if selected_model == "Gemini":
            with st.spinner("Thinking..."):
                response = gemini_client.models.generate_content(
                    model=selected_gemini_model,  # Use the selected Gemini model
                    contents=user_input
                )
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        elif selected_model == "DeepSeek":
            with st.spinner("Thinking..."):
                completion = deepseek_client.chat.completions.create(
                    model="deepseek/deepseek-chat:free",
                    messages=[
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                )
                st.session_state.chat_history.append({"role": "assistant", "content": completion.choices[0].message.content})

        # Rerun to update the UI with the new response
        st.rerun()