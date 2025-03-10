import streamlit as st
from styles import sidebar, custom_css
from pages.items import show_items_page
from pages.favorites import show_favorites_page
from pages.orders import show_orders_page
from pages.registration import registration_page
from pages.chat import render_chat_interface

if "user" not in st.session_state:
    st.session_state["user"] = None
    st.session_state["token"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "start"


sidebar(
    user=st.session_state["user"],
    token=st.session_state["token"],
    page_state=st.session_state
)

st.markdown(custom_css("assets/BG01.png"), unsafe_allow_html=True)


def start_page():
    st.image("assets/Emotion Potion.png", width=600)
    st.header("Hi everyone!")
    st.write("""
    Welcome to a website full of emotion! \n
    We are glad you came here.\n
    You are welcome to look inside, feel what you are missing,\n connect to the website from the side menu, 
    and order as you wish.\n
    We are here for you\n
    🫀
    Enjoy
    """)
    if st.button("see all items"):
        st.session_state["page"] = "items"
        st.rerun()


if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    start_page()
elif st.session_state["page"] == "items":
    show_items_page(token=st.session_state["token"])
elif st.session_state["page"] == "favorites":
    show_favorites_page(user=st.session_state["user"], token=st.session_state["token"])
elif st.session_state["page"] == "order":
    show_orders_page(user=st.session_state["user"], token=st.session_state["token"])
elif st.session_state["page"] == "chat":
    render_chat_interface()
elif st.session_state["page"] == "registration":
    registration_page()

else:
    start_page()
