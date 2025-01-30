import streamlit as st
import google.generativeai as generativeai

# Function to check API key validity
def is_valid_api_key(api_key):
    """Check if the provided API key is valid by making a simple test request."""
    try:
        generativeai.configure(api_key=api_key)
        model = generativeai.GenerativeModel("gemini-pro")
        response = model.generate_content("Hello")  # Test API call
        return bool(response)  # If response is valid, return True
    except Exception:
        return False  # Invalid API key

# Sidebar Component
def st_sidebar():
    with st.sidebar:
        st.title("AI Chatbot")
        st.text("Feel free to ask me anything! 😊")
        rate = st.slider("How much do you rate our App?", 0, 5, 0, step=1)
        if rate > 0:
            st.write("Thank you for your feedback! 🎉")

# Function to display chat messages
def display_message(role, text):
    """Display messages with distinct styles for User and Assistant."""
    color = "#0d6efd" if role == "user" else "#198754"
    align = "right" if role == "user" else "left"

    st.markdown(
        f"""
        <div style="display: flex; justify-content: {align}; margin: 5px 0;">
            <div style="background-color: {color}; color: white; padding: 12px; 
                        border-radius: 10px; max-width: 70%; font-size: 16px;">
                <strong>{role.upper()}:</strong> {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Chat Session Management
def session(session_key, user_prompt):
    """Handle chat session and display user & bot messages properly."""
    for message in st.session_state[session_key].history:
        role = "user" if message.role == "user" else "assistant"
        message_text = message.parts[0].text
        display_message(role, message_text)

    if user_prompt:
        display_message("user", user_prompt)

        # AI Response
        try:
            response = st.session_state[session_key].send_message(user_prompt)
            if response.candidates:
                assistant_text = response.candidates[0].content.parts[0].text
                display_message("assistant", assistant_text)
            else:
                st.error("No valid response from AI.")
        except Exception as e:
            st.error(f"Error during AI response: {e}")

# Main Function
def main():
    st.set_page_config(
        page_title="AI Chatbot",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("🤖 AI ChatBot using Google Gemini")

    # Request user to input their Google API key
    st.markdown("""
        🗝️ To use this chatbot, you need a Google Gemini API key.  
        **[Click here to enable Gemini API](https://console.cloud.google.com/marketplace/product/google/generativelanguage.googleapis.com?q=search&referrer=search&project=chatbot-449404&supportedpurview=project)**  
        Once enabled, enter your API key below:
    """, unsafe_allow_html=True)

    # API Key Input Field
    Google_API_KEY = st.text_input("Enter your Google Gemini API key:", type="password")

    if Google_API_KEY:
        if is_valid_api_key(Google_API_KEY):
            st.success("✅ API Key is valid! Reloading...")
            st.session_state["api_key"] = Google_API_KEY
            st.experimental_rerun()  # Reload the page when API key is valid
        else:
            st.error("❌ Invalid API Key! Please enter a valid key.")

    if "api_key" not in st.session_state:
        return  # Stop execution if API key is missing or invalid

    # Configure Google Gemini AI with the user's API key
    generativeai.configure(api_key=st.session_state["api_key"])

    llm = generativeai.GenerativeModel("gemini-pro")
    st_sidebar()

    # Initialize chat session
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = llm.start_chat(history=[])

    user_prompt = st.chat_input("Ask me anything...")
    if user_prompt is not None:
        session("chat_session", user_prompt=user_prompt)

# Run the main function
if __name__ == "__main__":
    main()
