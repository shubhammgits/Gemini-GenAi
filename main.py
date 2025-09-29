import os
import streamlit as st
from streamlit_option_menu import option_menu

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


