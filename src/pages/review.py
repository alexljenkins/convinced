import random
import requests
from time import sleep

import openai
import streamlit as st
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components

from src.database import update_entry, get_entries_for_voting, add_to_db_log
from src.elo import calculate_rating_change
from src.pages.styles import hide_default_style

def vote(session_state, db, winning_response, losing_response):
    rating_change = calculate_rating_change(winning_response[4], losing_response[4])
    
    # winner
    winning_response[4] = winning_response[4] + rating_change
    update_entry(db = db, id = winning_response[0], elo = winning_response[4], vote_count = winning_response[3])
    
    # loser
    losing_response[4] = losing_response[4] - rating_change
    update_entry(db = db, id = losing_response[0], elo = losing_response[4], vote_count = losing_response[3])

    add_to_db_log(db, winning_response, losing_response, rating_change)
    
    session_state.rating_change = rating_change


def review_page(session_state, db):
    hide_default_style()
    st.title("Review Page!")
    # if st.button("Homepage"):
    # session_state.page = "convince_me_page"
    # st.experimental_rerun()
    
    left_col, right_col = st.columns([100,100])
    
    left_response, right_response = get_entries_for_voting(db)
    session_state.left_response, session_state.right_response = left_response, right_response
    
    with left_col.container():
        left_container = st.container()
        display_response_to_review(left_container, left_response[1])
        left_score = st.empty()
    with right_col.container():
        right_container = st.container()
        display_response_to_review(right_container, right_response[1])
        right_score = st.empty()
    
    _, _, centre_left, _, _, _, _, centre_right, _, _ = st.columns(10)

    if centre_left.button("vote", key='left', on_click=vote(session_state, db, left_response, right_response)):
        session_state.winner = 'left'
        session_state.page = "reviewed_page"
        st.experimental_rerun()
        
    if centre_right.button("vote", key='right', on_click=vote(session_state, db, right_response, right_response)):
        session_state.winner = 'right'
        session_state.page = "reviewed_page"
        st.experimental_rerun()


def display_response_to_review(content, response):
    # content.header("Choice")
    content.write(f"<div style='text-align: left;'>{response}</div><br>", unsafe_allow_html=True)
