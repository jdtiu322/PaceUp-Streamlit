from __future__ import annotations

import streamlit as st

from components.hero import render_footer, render_register_hero
from services.firebase import register_user
from state import clear_register, go_to, set_flash, show_flash

def show_register() -> None:
    left, right = st.columns([0.92, 1.08], gap="small")
    with left:
        if st.session_state.clear_register_pending:
            clear_register()
            st.session_state.clear_register_pending = False
        with st.container(key="auth_panel"):
            st.markdown('<div class="panel-title">Register</div>', unsafe_allow_html=True)
            with st.container(key="register_switch", horizontal=True):
                st.markdown('<div class="switch-copy">Already have an account?</div>', unsafe_allow_html=True)
                if st.button("Sign In", key="register_switch_button", type="secondary"):
                    go_to("login")
            show_flash()
            with st.form("register_form", clear_on_submit=False):
                st.markdown('<div class="field-label">Full Name</div>', unsafe_allow_html=True)
                full_name = st.text_input("Full Name", placeholder="Your full name", key="reg_name", label_visibility="collapsed")
                st.markdown('<div class="field-label">Email Address</div>', unsafe_allow_html=True)
                email = st.text_input("Email Address", placeholder="name@example.com", key="reg_email", label_visibility="collapsed")
                st.markdown('<div class="field-label">Password</div>', unsafe_allow_html=True)
                password = st.text_input("Password", placeholder="At least 6 characters", type="password", key="reg_pass", label_visibility="collapsed")
                st.markdown('<div class="field-label">Confirm Password</div>', unsafe_allow_html=True)
                confirm = st.text_input("Confirm Password", placeholder="Repeat your password", type="password", key="reg_confirm", label_visibility="collapsed")
                submitted = st.form_submit_button("Create Account →", type="primary", use_container_width=True)
            if submitted:
                if not full_name or not email or not password or not confirm:
                    set_flash("error", "Fill in every field.")
                    st.rerun()
                if password != confirm:
                    set_flash("error", "Passwords do not match.")
                    st.rerun()
                if len(password) < 6:
                    set_flash("error", "Password must be at least 6 characters.")
                    st.rerun()
                user, error = register_user(email, password, full_name)
                if user:
                    st.session_state.clear_register_pending = True
                    set_flash("success", "Account created. You can sign in now.")
                    st.session_state.page = "login"
                    st.rerun()
                set_flash("error", error or "Registration failed.")
                st.rerun()
    with right:
        render_register_hero()
    render_footer()


# ── Onboarding ────────────────────────────────────────────────────────────────
