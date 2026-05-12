from __future__ import annotations

import html

import streamlit as st

VALID_LANDING_PAGES = {"home", "login", "register", "about", "contact", "onboarding", "chat"}


def _route_href(page: str) -> str:
    safe_page = page if page in VALID_LANDING_PAGES else "home"
    return f"?page={safe_page}"


def _route_link(label: str, page: str, css_class: str) -> None:
    st.markdown(
        (
            f'<a class="{html.escape(css_class, quote=True)}" '
            f'href="{html.escape(_route_href(page), quote=True)}" target="_self">'
            f"{html.escape(label)}</a>"
        ),
        unsafe_allow_html=True,
    )


def show_landing() -> None:
    st.markdown('<div class="landing-page-bg"></div>', unsafe_allow_html=True)

    with st.container(key="landing_nav"):
        brand_col, spacer_col, actions_col = st.columns([1.35, 2.85, 1.5], gap="small")
        with brand_col:
            st.markdown(
                """
                <div class="landing-brand">
                    <span class="landing-brand-mark">↗</span>
                    <span>PaceUp</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with spacer_col:
            st.markdown('<div class="landing-nav-spacer"></div>', unsafe_allow_html=True)
        with actions_col:
            with st.container(key="landing_nav_actions"):
                login_col, start_col = st.columns([.76, 1.24], gap="small")
                with login_col:
                    _route_link("Log in", "login", "landing-route-link landing-login-link")
                with start_col:
                    _route_link("Start training  →", "register", "landing-route-link landing-start-link")

    with st.container(key="landing_hero"):
        copy_col, visual_col = st.columns([1.04, .96], gap="large")
        with copy_col:
            st.markdown(
                """
                <div class="landing-copy">
                    <div class="landing-kicker"><span></span> Personal marathon coach · AI-powered</div>
                    <h1>Your<br/>marathon,<br/><em>paced</em> by AI.</h1>
                    <p>
                        PaceUp builds personalized training plans, calculates your pace zones,
                        and adapts every week to how your body actually feels — from couch to
                        5K to your first sub-3:30 marathon.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            cta_one, cta_two, _ = st.columns([.34, .27, .39], gap="small")
            with cta_one:
                _route_link("Get your plan free  →", "register", "landing-route-link landing-primary-link")
            with cta_two:
                _route_link("Try the chat", "login", "landing-route-link landing-secondary-link")
            st.markdown(
                """
                <div class="landing-stats">
                    <div><strong>5K → 42K</strong><span>Race distances</span></div>
                    <div><strong>16 wks</strong><span>Avg. plan length</span></div>
                    <div><strong>24/7</strong><span>Coach availability</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with visual_col:
            st.markdown(
                """
                <div class="landing-visual">
                    <div class="plan-toast plan-toast-top"><span></span> Plan adapted +12% volume</div>
                    <div class="plan-toast plan-toast-left"><span></span> Long run · Sun · 22 km</div>
                    <div class="plan-card">
                        <div class="plan-card-top">
                            <div>Week 7 of 16 · Berlin Marathon</div>
                            <span>● Live plan</span>
                        </div>
                        <div class="plan-metric">
                            <strong>42</strong><span>km / week</span><em>▲ 4 km vs last week</em>
                        </div>
                        <div class="plan-chart">
                            <div><i style="height:34%"></i><span>Mon</span></div>
                            <div><i style="height:60%"></i><span>Tue</span></div>
                            <div><i style="height:0%"></i><span>Wed</span></div>
                            <div><i style="height:49%"></i><span>Thu</span></div>
                            <div><i style="height:25%"></i><span>Fri</span></div>
                            <div><i style="height:0%"></i><span>Sat</span></div>
                            <div><i style="height:98%"></i><span>Sun</span></div>
                        </div>
                        <div class="plan-divider"></div>
                        <div class="plan-card-bottom">
                            <span><strong>Tempo</strong> · 6 km @ 4:35/km</span>
                            <span>Long run <strong>22 km</strong></span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
