from __future__ import annotations

import html
import streamlit as st

from config import FITNESS_MAP, ONBOARDING_DAY_OPTIONS, ONBOARDING_GOAL_OPTIONS, ONBOARDING_SEX_OPTIONS, normalize_fitness_level
from services.firebase import build_chat_profile, get_user_profile, save_onboarding_data
from state import prime_onboarding_state, toggle_training_day

def show_onboarding() -> None:
    user = st.session_state.user
    profile = get_user_profile(user.uid)
    prime_onboarding_state(user.uid, profile)

    left, right = st.columns([0.18, 0.82], gap="large")

    with left:
        st.markdown(
            """
            <div class="ob-sidebar">
                <div class="ob-sidebar-top">
                    <div class="ob-sidebar-brand">PaceUp</div>
                    <div class="ob-sidebar-title">SHARP<br/>MEETS<br/>PERFORMANCE.</div>
                    <div class="ob-sidebar-copy">
                        Set your coordinates. Our AI engine will calibrate the most efficient path to your personal best.
                    </div>
                </div>
                <div class="ob-sidebar-footer">
                    <div class="ob-phase-bar">
                        <div class="ob-phase-line"></div>
                        <div class="ob-phase-label">Onboarding Phase 01</div>
                    </div>
                    <div class="ob-copyright">© 2024 PACEUP HIGH PERFORMANCE SYSTEMS</div>
                </div>
                <div class="ob-kinetic"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="ob-form-header">
                <div class="ob-form-title">Create Your Profile</div>
                <div class="ob-form-sub">Complete your details to generate your tailored marathon preparation plan.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(key="ob_formwrap"):
            st.markdown(
                """
                <div class="ob-section-header">
                    <div class="ob-section-title">Personal Info</div>
                    <div class="ob-section-line"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            personal_c1, personal_c2, personal_c3 = st.columns(3, gap="large")
            with personal_c1:
                st.markdown('<div class="ob-field-label">Age</div>', unsafe_allow_html=True)
                st.text_input("Age", placeholder="28", key="ob_age", label_visibility="collapsed")
            with personal_c2:
                st.markdown('<div class="ob-field-label">Weight (KG)</div>', unsafe_allow_html=True)
                st.text_input("Weight (KG)", placeholder="72", key="ob_weight", label_visibility="collapsed")
            with personal_c3:
                st.selectbox("Sex", ONBOARDING_SEX_OPTIONS, key="ob_sex", label_visibility="visible")

            st.markdown(
                """
                <div class="ob-section-header" style="margin-top:3.1rem;">
                    <div class="ob-section-title">Running Goals</div>
                    <div class="ob-section-line"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            goals_top_left, goals_top_right = st.columns(2, gap="large")
            with goals_top_left:
                st.markdown('<div class="ob-field-label">Fitness Level</div>', unsafe_allow_html=True)
                with st.container(key="ob_fit_toggle"):
                    fit_c1, fit_c2, fit_c3 = st.columns(3, gap="small")
                    with fit_c1:
                        if st.button(
                            "NOVICE",
                            key="ob_fit_novice",
                            type="primary" if st.session_state.ob_fitness == "NOVICE" else "secondary",
                            use_container_width=True,
                        ):
                            st.session_state.ob_fitness = "NOVICE"
                            st.rerun()
                    with fit_c2:
                        if st.button(
                            "INTER",
                            key="ob_fit_inter",
                            type="primary" if st.session_state.ob_fitness == "INTER" else "secondary",
                            use_container_width=True,
                        ):
                            st.session_state.ob_fitness = "INTER"
                            st.rerun()
                    with fit_c3:
                        if st.button(
                            "ELITE",
                            key="ob_fit_elite",
                            type="primary" if st.session_state.ob_fitness == "ELITE" else "secondary",
                            use_container_width=True,
                        ):
                            st.session_state.ob_fitness = "ELITE"
                            st.rerun()
                st.markdown(
                    f'<div class="ob-fit-note">Selected: {html.escape(st.session_state.ob_fitness)} - {html.escape(FITNESS_MAP[st.session_state.ob_fitness])}</div>',
                    unsafe_allow_html=True,
                )
            with goals_top_right:
                st.selectbox("Goal Distance", ONBOARDING_GOAL_OPTIONS, key="ob_goal_distance", label_visibility="visible")

            goals_bottom_left, goals_bottom_right = st.columns(2, gap="large")
            with goals_bottom_left:
                st.date_input("Target Race Date", key="ob_goal_race_date", label_visibility="visible")
            with goals_bottom_right:
                st.markdown('<div class="ob-field-label">Current Weekly KM</div>', unsafe_allow_html=True)
                st.text_input("Current Weekly KM", placeholder="25", key="ob_current_weekly_km", label_visibility="collapsed")

            st.markdown(
                """
                <div class="ob-section-header" style="margin-top:3.1rem;">
                    <div class="ob-section-title">Training Schedule</div>
                    <div class="ob-section-line"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('<div class="ob-field-label">Training Days</div>', unsafe_allow_html=True)
            with st.container(key="ob_days"):
                day_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 4], gap="small")
                for (day_name, short_label), col in zip(ONBOARDING_DAY_OPTIONS, day_cols[:7]):
                    with col:
                        if st.button(
                            short_label,
                            key=f"ob_day_{day_name}",
                            type="primary" if day_name in st.session_state.ob_training_days else "secondary",
                        ):
                            toggle_training_day(day_name)
                            st.rerun()

            st.selectbox(
                "Preferred Long Run Day",
                [day for day, _label in ONBOARDING_DAY_OPTIONS],
                key="ob_preferred_long_run_day",
                label_visibility="visible",
            )

            st.markdown('<div class="ob-field-label" style="margin-top:1rem;">Recent Race Time (optional)</div>', unsafe_allow_html=True)
            st.text_input(
                "Recent Race Time (optional)",
                placeholder="e.g. 25:30 for a 5K",
                key="ob_recent_race_time",
                label_visibility="collapsed",
            )

            st.checkbox("I currently have an injury or physical limitation", key="ob_injury_flag")

            with st.container(key="ob_submit"):
                submitted = st.button("Save and Start Training", type="primary", use_container_width=True)
            st.markdown(
                '<div class="ob-terms">By clicking, you agree to our <span>Athletic Terms of Service</span> and high-performance guidelines.</div>',
                unsafe_allow_html=True,
            )

            if submitted:
                errors = []
                age_raw = str(st.session_state.ob_age).strip()
                weight_raw = str(st.session_state.ob_weight).strip()
                weekly_km_raw = str(st.session_state.ob_current_weekly_km).strip()
                training_days = st.session_state.ob_training_days

                try:
                    age = int(age_raw)
                    if age < 10 or age > 100:
                        errors.append("Age must be between 10 and 100.")
                except ValueError:
                    errors.append("Enter a valid age.")

                try:
                    weight = float(weight_raw)
                    if weight < 30 or weight > 200:
                        errors.append("Weight must be between 30 and 200 KG.")
                except ValueError:
                    errors.append("Enter a valid weight in KG.")

                try:
                    current_weekly_km = float(weekly_km_raw or "0")
                    if current_weekly_km < 0 or current_weekly_km > 300:
                        errors.append("Current weekly KM must be between 0 and 300.")
                except ValueError:
                    errors.append("Enter a valid weekly KM value.")

                if not training_days:
                    errors.append("Select at least one training day.")

                if errors:
                    for message in errors:
                        st.error(message)
                else:
                    try:
                        save_onboarding_data(
                            user.uid,
                            {
                                "age": age,
                                "weight_kg": weight,
                                "sex": st.session_state.ob_sex,
                                "fitness_level": FITNESS_MAP[normalize_fitness_level(st.session_state.ob_fitness)],
                                "goal_distance": st.session_state.ob_goal_distance,
                                "goal_race_date": st.session_state.ob_goal_race_date.isoformat(),
                                "current_weekly_km": current_weekly_km,
                                "recent_race_time": st.session_state.ob_recent_race_time.strip() or None,
                                "training_days_per_week": len(training_days),
                                "training_days": training_days,
                                "preferred_long_run_day": st.session_state.ob_preferred_long_run_day,
                                "injury_flag": bool(st.session_state.ob_injury_flag),
                            },
                        )
                        st.session_state.user_profile = build_chat_profile(user)
                        st.session_state.page = "chat"
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Failed to save profile: {exc}")

        st.markdown('<div class="ob-map-deco"></div>', unsafe_allow_html=True)


# ── Chat ──────────────────────────────────────────────────────────────────────

