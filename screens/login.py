from __future__ import annotations

import streamlit as st

from components.hero import render_footer, render_login_hero
from services.firebase import check_onboarding_status, login_user
from state import go_to, set_flash, show_flash

def show_login() -> None:
    left, right = st.columns([0.92, 1.08], gap="small")
    with left:
        if st.session_state.clear_login_password_pending:
            st.session_state.login_password = ""
            st.session_state.clear_login_password_pending = False
        with st.container(key="login_shell"):
            st.markdown('<div class="login-heading">Sign In</div>', unsafe_allow_html=True)
            with st.container(key="login_switch", horizontal=True):
                st.markdown('<div class="login-sub">Don\'t have an account?</div>', unsafe_allow_html=True)
                if st.button("Create Account", key="login_switch_button", type="secondary"):
                    go_to("register")
            show_flash()
            with st.form("login_form", clear_on_submit=False):
                st.markdown('<div class="field-label">Email Address</div>', unsafe_allow_html=True)
                email = st.text_input("Email", placeholder="name@example.com", key="login_email", label_visibility="collapsed")
                st.markdown('<div class="password-meta"><div class="field-label">Password</div><div class="forgot-link">Forget Password?</div></div>', unsafe_allow_html=True)
                password = st.text_input("Password", placeholder="Enter your password", type="password", key="login_password", label_visibility="collapsed")
                submitted = st.form_submit_button("Login →", type="primary", use_container_width=True)
            if submitted:
                if not email or not password:
                    set_flash("error", "Enter both email and password.")
                    st.rerun()
                user, error = login_user(email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.clear_login_password_pending = True
                    st.session_state.page = "chat" if check_onboarding_status(user.uid) else "onboarding"
                    st.rerun()
                set_flash("error", error or "Account not found.")
                st.rerun()
            st.markdown("""
            <div class="alt-divider">Or continue with</div>
            <div class="alt-buttons">
                <div class="alt-btn">Google</div>
                <div class="alt-btn">Apple</div>
            </div>
            """, unsafe_allow_html=True)
    with right:
        render_login_hero()
    render_footer()


# ── Register ──────────────────────────────────────────────────────────────────
