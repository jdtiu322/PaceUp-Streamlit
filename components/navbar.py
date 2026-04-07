from __future__ import annotations

import streamlit as st

from config import LOGO_IMAGE
from state import get_home_page, go_to, logout_user

def render_nav() -> None:
    active_page = st.session_state.page
    home_active = active_page not in {"about", "contact"}
    with st.container(key="top_nav"):
        left, mid, right = st.columns([1.2, 1.45, 0.85], gap="small")
        with left:
            if LOGO_IMAGE:
                st.markdown(f'<div class="brand"><img class="brand-logo" src="data:image/png;base64,{LOGO_IMAGE}" alt="PaceUp"/></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="brand"><div class="brand-wordmark"><span class="brand-pace">PACE</span><span class="brand-up">UP</span></div></div>', unsafe_allow_html=True)
        with mid:
            with st.container(key="nav_links", horizontal=True):
                if st.button("Home", key="nav_home_link", type="primary" if home_active else "secondary"):
                    go_to(get_home_page())
                if st.button("About", key="nav_about_link", type="primary" if active_page == "about" else "secondary"):
                    go_to("about")
                if st.button("Contact", key="nav_contact_link", type="primary" if active_page == "contact" else "secondary"):
                    go_to("contact")
        with right:
            a, b = st.columns(2, gap="small")
            if st.session_state.user:
                with a:
                    st.button("Dashboard", key="nav_dashboard", disabled=True, type="secondary", use_container_width=True)
                with b:
                    if st.button("Sign out", key="nav_signout", type="primary", use_container_width=True):
                        logout_user()
            else:
                with a:
                    if st.button("Sign In", key="nav_login", type="secondary", use_container_width=True):
                        go_to("login")
                with b:
                    if st.button("Register", key="nav_register", type="primary", use_container_width=True):
                        go_to("register")


