import os
import time
import streamlit as st
from streamlit_option_menu import option_menu

from gemini_utility import load_gemini_pro_model, retry_on_rate_limit

working_directory = os.path.dirname(os.path.abspath(__file__))


st.set_page_config(
    page_title="Gemini GenAI", 
    page_icon="🧠",
    layout="centered"
)


with st.sidebar:
    selected = option_menu("Gemini GenAI",
        options=["ChatBot", "Image Captioning", "Embed text", "Ask me anything"],
        menu_icon = 'robot', icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
        default_index=0
)



def translate_role_from_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role


# Wrapper function for sending messages with retry logic
@retry_on_rate_limit
def send_message_with_retry(chat_session, prompt):
    return chat_session.send_message(prompt)


if selected == "ChatBot":
    
    model = load_gemini_pro_model()

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("🤖 ChatBot")

    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_from_streamlit(message.role)):
            st.markdown(message.parts[0].text)
    


    user_prompt = st.chat_input("Ask me anything...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        try:
            gemini_response = send_message_with_retry(st.session_state.chat_session, user_prompt)
            
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)
        except Exception as e:
            if "429" in str(e):
                st.error("Rate limit exceeded. Please wait a moment and try again.")
            else:
                st.error(f"An error occurred: {str(e)}")