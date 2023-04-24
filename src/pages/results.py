import random
import requests
import openai

import streamlit as st
from streamlit_lottie import st_lottie

from src.database import save_entry, check_entry_against_db, get_entries_for_voting
from src.elo import starting_elo, calculate_rating_change
from src.ask_ai import ask_ai, get_api_key
from src.pages.styles import hide_default_style

def results_page():
    hide_default_style()
    st.title("Results Page!")
    
    display_results()
    
    if st.button("Review other responses"):
        st.session_state.page = "review_page"
        st.experimental_rerun()

def display_results():
    st.write(f"<div style='text-align: center;'>{st.session_state.response}</div><br><br><br><br>", unsafe_allow_html=True)