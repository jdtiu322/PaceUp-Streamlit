from __future__ import annotations

import streamlit as st

from services.firebase import register_user
from state import clear_register, go_to, set_flash, show_flash


def show_register() -> None:
    if st.session_state.clear_register_pending:
        clear_register()
        st.session_state.clear_register_pending = False

    st.markdown('<div class="auth-page-bg"></div>', unsafe_allow_html=True)

    with st.container(key="auth_hero"):
        st.markdown(
            """
            <div class="auth-brand-mini">
                <span class="auth-brand-mark">&nearr;</span>
                <span>PaceUp</span>
            </div>
            <div class="auth-kicker"><span></span> Create your account</div>
            <h1 class="auth-headline">Start running smarter.</h1>
            <p class="auth-sub">Free forever. No credit card. Get your first personalized training week in under two minutes.</p>
            """,
            unsafe_allow_html=True,
        )

        show_flash()

        with st.form("register_form", clear_on_submit=False):
            st.markdown('<div class="auth-label">Full name</div>', unsafe_allow_html=True)
            full_name = st.text_input(
                "Full name",
                placeholder="Maya Rodriguez",
                key="reg_name",
                label_visibility="collapsed",
            )
            st.markdown('<div class="auth-label">Email</div>', unsafe_allow_html=True)
            email = st.text_input(
                "Email",
                placeholder="you@example.com",
                key="reg_email",
                label_visibility="collapsed",
            )
            st.markdown('<div class="auth-label">Password</div>', unsafe_allow_html=True)
            password = st.text_input(
                "Password",
                placeholder="At least 8 characters",
                type="password",
                key="reg_pass",
                label_visibility="collapsed",
            )
            st.markdown(
                '<div class="auth-rule-hint">Use 8+ characters with letters, numbers, and a symbol.</div>',
                unsafe_allow_html=True,
            )
            agreed = st.checkbox(
                "I agree to PaceUp's [Terms](?page=terms) and [Privacy Policy](?page=privacy), and understand PaceUp is not a medical advisor.",
                key="reg_agree",
            )
            submitted = st.form_submit_button("Create account ->", type="primary", use_container_width=True)

        if submitted:
            if not full_name or not email or not password:
                set_flash("error", "Fill in every field.")
                st.rerun()
            if len(password) < 8:
                set_flash("error", "Password must be at least 8 characters.")
                st.rerun()
            if not agreed:
                set_flash("error", "Please agree to the Terms and Privacy Policy.")
                st.rerun()
            user, error = register_user(email, password, full_name)
            if user:
                st.session_state.clear_register_pending = True
                set_flash("success", "Account created. You can sign in now.")
                go_to("login")
            set_flash("error", error or "Registration failed.")
            st.rerun()

        st.markdown(
            '<div class="auth-foot">Already a runner here? <a href="?page=login" target="_self">Sign in</a></div>',
            unsafe_allow_html=True,
        )
