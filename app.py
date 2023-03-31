import random
import requests
import streamlit as st
from streamlit_lottie import st_lottie


st.set_page_config(page_title = "Hello World", page_icon = ":smiley:", layout = "centered")


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


monster = random.choice(["https://assets1.lottiefiles.com/private_files/lf30_wggd72cc.json", "https://assets1.lottiefiles.com/private_files/lf30_gs9tkudw.json"])
# st.subheader("Hi")
st.title("convince.me")
st.write("write")
user_input = st.text_area(label = 'Write your response here and hit enter', label_visibility = 'collapsed', placeholder='write here...', height=200)
lottie_coding = load_lottieurl(monster)
st_lottie(lottie_coding, speed=1, key="monster") # height=200

