from __future__ import annotations

import html
import streamlit as st

from components.hero import render_footer

def show_placeholder_page(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="placeholder-page">
            <div class="placeholder-card">
                <div class="placeholder-title">{html.escape(title)}</div>
                <div class="placeholder-copy">{html.escape(body)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_footer()


# ── Login ─────────────────────────────────────────────────────────────────────
