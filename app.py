from __future__ import annotations

import streamlit as st

from components.navbar import render_nav
from components.styles import inject_styles
from screens.chat import show_chat
from screens.login import show_login
from screens.onboarding import show_onboarding
from screens.placeholder import show_placeholder_page
from screens.register import show_register
from services.firebase import init_firebase
from state import init_state, restore_saved_session

st.set_page_config(
    page_title="PaceUp",
    page_icon=":runner:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_firebase()
init_state()
restore_saved_session()
inject_styles()
render_nav()

if st.session_state.page == "about":
    show_placeholder_page("About", "This is about page")
elif st.session_state.page == "contact":
    show_placeholder_page("Contact", "This is contact page")
elif st.session_state.user:
    if st.session_state.page == "onboarding":
        show_onboarding()
    else:
        show_chat()
elif st.session_state.page == "register":
    show_register()
else:
    show_login()
