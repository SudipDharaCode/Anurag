import streamlit as st
from streamlit_mic_recorder import speech_to_text

#

st.write("Convert speech to text:")
text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')


st.write(text)