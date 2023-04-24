import random
import requests
import openai
import time
import streamlit as st
from streamlit_lottie import st_lottie

from src.database import save_entry, db_connect, check_entry_against_db
from src.elo import starting_elo, calculate_rating_change
from src.ask_ai import ask_ai, get_api_key
from src.pages.styles import hide_default_style


def convince_me_page(monster, db):
    hide_default_style()
    
    left_container, right_container = st.columns([1,2])
    with left_container.container():
        display_moster(monster)
    with right_container.container():
        st.title("convince.me")
        user_interaction(db)


def display_moster(monster_code):
    st_lottie(monster_code, speed=1, key="monster")


def user_interaction(db):
    st.session_state.user_input = st.text_area(label = 'Write your response here and hit enter', label_visibility = 'collapsed', placeholder='convince me here...', height=200)
    
    # Add a button to send user input to a variable
    if st.button('Send'):
        with st.spinner('Hmm...'):
            st.session_state.response, should_save = handle_response(db)

        if should_save:
            # Save user input and AI response in database
            save_entry(db, st.session_state.user_input, st.session_state.response, starting_elo())
        
        st.session_state.page = "results_page"
        st.experimental_rerun()


def too_short_validation(user_input) -> bool:
    word_count = len(user_input.split())
    return word_count < 10

def too_long_validation(user_input) -> bool:
    word_count = len(user_input.split())
    return word_count > 200


def handle_response(user_input, db):
    if too_short_validation(user_input):
        return f"Your answer is too short. Please write at least 10 words and no more than 200 words.", False
    
    if too_long_validation(user_input):
        return f"Your answer is too long. Please write at least 10 words and no more than 200 words.", False

    existing_response = check_entry_against_db(db, user_input)
    if existing_response:
        return f"I've heard that before... I'll tell you again:\n{existing_response}", False
    
    # if all checks pass, ask AI for a response
    response = ask_ai(user_input)
    
    return response, True