from __future__ import annotations

import streamlit as st

from services.firebase import check_onboarding_status, login_user
from state import set_flash, show_flash


def show_login() -> None:
    if st.session_state.clear_login_password_pending:
        st.session_state.login_password = ""
        st.session_state.clear_login_password_pending = False

    st.markdown('<div class="auth-page-bg auth-login-page"></div>', unsafe_allow_html=True)

    with st.container(key="auth_hero"):
        st.markdown(
            """
            <div class="auth-brand-mini">
                <span class="auth-brand-mark">&nearr;</span>
                <span>PaceUp</span>
            </div>
            <div class="auth-kicker"><span></span> Welcome back</div>
            <h1 class="auth-headline">Pick up your next run.</h1>
            <p class="auth-sub">Continue your plan, training conversations, and race-day prep.</p>
            """,
            unsafe_allow_html=True,
        )

        show_flash()

        with st.form("login_form", clear_on_submit=False):
            st.markdown('<div class="auth-label">Email</div>', unsafe_allow_html=True)
            email = st.text_input(
                "Email",
                placeholder="you@example.com",
                key="login_email",
                label_visibility="collapsed",
            )
            st.markdown(
                '<div class="auth-label-row"><span class="auth-label">Password</span><span class="auth-forgot">Forgot password?</span></div>',
                unsafe_allow_html=True,
            )
            password = st.text_input(
                "Password",
                placeholder="Enter your password",
                type="password",
                key="login_password",
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button("Sign in ->", type="primary", use_container_width=True)

        if submitted:
            if not email or not password:
                set_flash("error", "Enter both email and password.")
                st.rerun()
            user, error, refresh_token = login_user(email, password)
            if user:
                st.session_state.user = user
                st.session_state.pending_auth_token = refresh_token
                st.session_state.signed_out = False
                st.session_state.auth_restore_attempted = False
                st.session_state.auth_restore_attempts = 0
                st.session_state.clear_login_password_pending = True
                onboarding_done = check_onboarding_status(user.uid)
                st.session_state.onboarding_completed = onboarding_done
                st.session_state.page = "chat" if onboarding_done else "onboarding"
                st.rerun()
            set_flash("error", error or "Account not found.")
            st.rerun()

        st.markdown(
            '<div class="auth-foot">New to PaceUp? <a href="?page=register" target="_self">Create account</a></div>',
            unsafe_allow_html=True,
        )
