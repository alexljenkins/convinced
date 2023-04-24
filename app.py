# streamlit run app.py
import random
import requests
import openai

import streamlit as st

from src.database import db_connect
from src.ask_ai import get_api_key
from src.pages.convince_me import convince_me_page
from src.pages.review import review_page
from src.pages.results import results_page
from src.pages.reviewed import reviewed_page



# https://www.youtube.com/watch?v=Yd_W0sU1Fx4 -- you can have multiple pages in streamlit


def make_monster_choice():
    monster_url = random.choice(["https://assets1.lottiefiles.com/private_files/lf30_wggd72cc.json", "https://assets1.lottiefiles.com/private_files/lf30_gs9tkudw.json"])
    monster_code = load_lottieurl(monster_url)
    return monster_code

def load_lottieurl(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


def main_app(monster, db):
    st.set_page_config(page_title = "convince.me", page_icon = ":smiley:", layout = "wide", initial_sidebar_state = 'collapsed')
    global session_state
    session_state = st.session_state
    if not hasattr(session_state, "page"):
        session_state.initialized = True
        session_state.page = "convince_me_page"
        
    with st.sidebar:
        st.header("Navigation")
        if st.button("Home"):
            session_state.page = "convince_me_page"
        if st.button("Review"):
            session_state.page = "review_page"

    # Display the appropriate page
    if session_state.page == "convince_me_page":
        convince_me_page(session_state, monster, db)
    elif session_state.page == "results_page":
        results_page(session_state)
    elif session_state.page == "review_page":
        review_page(session_state, db)
    elif session_state.page == "reviewed_page":
        reviewed_page(session_state)

if __name__ == "__main__":
    monster = make_monster_choice()
    db = db_connect()
    openai.api_key = get_api_key("api_key")
    # print(openai.Model.list())
    # layout_page(monster, db)
    
    main_app(monster, db)
