import random
import requests
import openai

import streamlit as st
from streamlit_lottie import st_lottie

from src.database import save_entry, check_entry_against_db, get_entries_for_voting
from src.elo import starting_elo, calculate_rating_change
from src.ask_ai import ask_ai, get_api_key
from src.pages.styles import hide_default_style

def review_page(session_state):
    hide_default_style()
    st.title("Review Page!")
    if st.button("Homepage"):
        session_state.page = "convince_me_page"
        st.experimental_rerun()
