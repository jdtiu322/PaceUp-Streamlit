from __future__ import annotations

import html
import streamlit as st

from config import RUNNER_IMAGE

def render_login_hero() -> None:
    image = f"url('data:image/jpeg;base64,{RUNNER_IMAGE}')" if RUNNER_IMAGE else "linear-gradient(135deg, #000568 0%, #1b237e 100%)"
    st.markdown(f"""
    <div class="login-hero" style="background-image:{image};">
        <div class="login-hero-ring"></div>
        <div class="login-hero-content">
            <div class="login-hero-stripe"></div>
            <div class="login-hero-title">PRECISION<br/>VELOCITY.</div>
            <div class="login-hero-copy">
                Unlock your true potential with data-driven performance tracking engineered for the elite.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_register_hero() -> None:
    image = f"url('data:image/jpeg;base64,{RUNNER_IMAGE}')" if RUNNER_IMAGE else "linear-gradient(135deg, #000568 0%, #ff5722 100%)"
    st.markdown(f"""
    <div class="login-hero" style="background-image:{image};">
        <div class="login-hero-ring"></div>
        <div class="login-hero-content">
            <div class="login-hero-stripe"></div>
            <div class="login-hero-title">BUILD YOUR<br/>PROFILE.</div>
            <div class="login-hero-copy">
                Set your goals, tell us your pace, and let PaceUp build a training plan designed around your life.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer() -> None:
    st.markdown("""
    <div class="site-footer">
        <div class="footer-brand">PaceUp</div>
        <div class="footer-copy">© 2025 PaceUp. All rights reserved.</div>
        <div class="footer-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Training FAQ</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


