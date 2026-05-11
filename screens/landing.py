from __future__ import annotations

import streamlit as st

from state import route_link


def show_landing() -> None:
    st.markdown('<div class="landing-page-bg"></div>', unsafe_allow_html=True)

    with st.container(key="landing_nav"):
        brand_col, links_col, actions_col = st.columns([1.35, 2.6, 1.35], gap="small")
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
        with links_col:
            st.markdown(
                """
                <div class="landing-links">
                    <span>Features</span>
                    <span>Try the coach</span>
                    <span>How it works</span>
                    <span>Plans</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with actions_col:
            login_col, start_col = st.columns([.76, 1.24], gap="small")
            with login_col:
                route_link("Log in", "login", "landing-route-link landing-login-link")
            with start_col:
                route_link("Start training  →", "register", "landing-route-link landing-start-link")

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
                route_link("Get your plan free  →", "register", "landing-route-link landing-primary-link")
            with cta_two:
                route_link("Try the chat", "login", "landing-route-link landing-secondary-link")
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
