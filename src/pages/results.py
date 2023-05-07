import streamlit as st
import json

from src.pages.styles import hide_default_style
from src.message_log import parse_teacher_reponse


def results_page():
    hide_default_style()
    st.title("Results Page!")
    
    display_results()
    
    if st.button("See what others have tried"):
        st.session_state.page = "review_page"
        st.experimental_rerun()


def display_results():
    st.markdown(f"{st.session_state.monster_response}", unsafe_allow_html=True)
    st.table(data=st.session_state.teacher_response.df_format())
    # st.write(f"{st.session_state.teacher_response}")