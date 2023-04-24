from time import sleep
import random

import streamlit as st

from src.pages.styles import hide_default_style

def reviewed_page(session_state):
    hide_default_style()
    st.title("Review Page!")

    l_col, r_col = st.columns(2)
    
    # left_response, right_response = session_state.left_response, session_state.right_response
    
    with l_col.container():
        l_con = st.container()
        # NOTE: no idea why content is still being displayed when this is commented out
        # display_response_to_review(l_con, left_response[1])
        left_score = st.empty()
    with r_col.container():
        right_container = st.container()
        # NOTE: no idea why content is still being displayed when this is commented out
        # display_response_to_review(right_container, right_response[1])
        right_score = st.empty()
    
    _, _, centre_left, _, _, _, _, centre_right, _, _ = st.columns(10)

    if session_state.winner == 'left':
        centre_left.write(f"<p style='text-align: center;'>+{session_state.rating_change}</div><br>", unsafe_allow_html=True)
        centre_right.write(f"<p style='text-align: center;'>-{session_state.rating_change}</div><br>", unsafe_allow_html=True)
        display_next_review(session_state)

    if session_state.winner == 'right':
        centre_left.write(f"<p style='text-align: center;'>-{session_state.rating_change}</div><br>", unsafe_allow_html=True)
        centre_right.write(f"<p style='text-align: center;'>+{session_state.rating_change}</div><br>", unsafe_allow_html=True)
        display_next_review(session_state)


def maybe_play_balloons():
    if 'balloons' not in st.session_state:
        st.balloons()
        st.session_state.balloons = True
    elif random.randint(1,4) == 1:
        st.balloons()

def display_next_review(session_state):
        session_state.page = "review_page"
        
        maybe_play_balloons()
        
        _, ty, _ = st.columns(3)
        ty.success('Thank you for voting!', icon='🥳')
        sleep(1.5)
        st.experimental_rerun()
        
