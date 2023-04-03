import random
import requests
import openai

import streamlit as st
from streamlit_lottie import st_lottie

from src.database import save_entry, db_connect, check_entry_against_db
from src.elo import starting_elo, calculate_rating_change
from src.ask_ai import ask_ai, get_api_key


def make_monster_choice():
    monster_url = random.choice(["https://assets1.lottiefiles.com/private_files/lf30_wggd72cc.json", "https://assets1.lottiefiles.com/private_files/lf30_gs9tkudw.json"])
    monster_code = load_lottieurl(monster_url)
    return monster_code


st.set_page_config(page_title = "convince.me", page_icon = ":smiley:", layout = "centered")

def hide_default_style():
    # --- HIDE STREAMLIT STYLE ---
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)


def load_lottieurl(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def user_interaction(db):
    user_input = st.text_area(label = 'Write your response here and hit enter', label_visibility = 'collapsed', placeholder='convince me here...', height=200)
    
    # Add a button to send user input to a variable
    if st.button('Send'):
        with st.spinner('Hmm...'):
            response, should_save = handle_response(user_input, db)
        
        st.write(f"<div style='text-align: center;'>{response}</div>", unsafe_allow_html=True)
    
        if should_save:
            # Save user input and AI response in database
            save_entry(db, user_input, response, starting_elo())


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



def display_moster(monster_code):
    st_lottie(monster_code, speed=1, key="monster")


def layout_page(monster, db):
    hide_default_style()
    st.title("convince.me")
    st.write("write")
    user_interaction(db)
    display_moster(monster)


if __name__ == "__main__":
    monster = make_monster_choice()
    db = db_connect()
    openai.api_key = get_api_key("api_key")
    # print(openai.Model.list())
    layout_page(monster, db)
