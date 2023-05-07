import logging

import streamlit as st

from src.database import update_entry, get_entries_for_voting, add_to_db_log
from src.elo import calculate_rating_change
from src.pages.styles import hide_default_style

logger = logging.getLogger(__name__)

def vote(db, winning_response, losing_response):
    rating_change = calculate_rating_change(winning_response[5], losing_response[5])
    
    # winner
    winning_response[5] += rating_change
    update_entry(db = db, id = winning_response[0], elo = winning_response[5], vote_count = winning_response[4] + 1)
    
    # loser
    losing_response[5] -= rating_change
    update_entry(db = db, id = losing_response[0], elo = losing_response[5], vote_count = losing_response[4] + 1)

    add_to_db_log(db, winning_response, losing_response, rating_change)
    logger.info(f"\nWinner: {[winning_response[index] for index in [0,4,5]]}\nLoser: {[losing_response[index] for index in [0,4,5]]}\nRating Change: {rating_change}")
    
    # st.session_state.rating_change = rating_change


def review_page(db):
    hide_default_style()
    st.title("Review Page!")
    # if st.button("Homepage"):
    # session_state.page = "convince_me_page"
    # st.experimental_rerun()
    
    left_col, right_col = st.columns([100,100])
    
    st.session_state.left_response, st.session_state.right_response = get_entries_for_voting(db)
    
    with left_col.container():
        left_container = st.container()
        display_response_to_review(left_container, st.session_state.left_response[1])
        left_score = st.empty()
    with right_col.container():
        right_container = st.container()
        display_response_to_review(right_container, st.session_state.right_response[1])
        right_score = st.empty()
    
    _, _, centre_left, _, _, _, _, centre_right, _, _ = st.columns(10)

    if centre_left.button("vote", key='left'):  #, on_click=vote(db, left_response, right_response)):
        vote(db, st.session_state.left_response, st.session_state.right_response)
        st.session_state.winner = 'left'
        st.session_state.page = "reviewed_page"
        st.experimental_rerun()
        
    if centre_right.button("vote", key='right'):  #, on_click=vote(db, right_response, left_response)):
        vote(db, st.session_state.right_response, st.session_state.left_response)
        st.session_state.winner = 'right'
        st.session_state.page = "reviewed_page"
        st.experimental_rerun()


def display_response_to_review(content, response):
    # content.header("Choice")
    content.write(f"""<div style='text-align: left;'>{response}</div><br>""", unsafe_allow_html=True)
