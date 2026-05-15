from __future__ import annotations

import html
import re
from datetime import date

import streamlit as st

from config import FITNESS_MAP, ONBOARDING_DAY_OPTIONS, ONBOARDING_GOAL_OPTIONS, ONBOARDING_SEX_OPTIONS, normalize_fitness_level
from services.firebase import build_chat_profile, get_user_profile, save_onboarding_data
from services.telemetry import log_event
from state import go_to, prime_onboarding_state, toggle_training_day


RECENT_RACE_TIME_PATTERN = re.compile(
    r"^(?:(?:5k|10k|half marathon|marathon|full marathon)\s+)?(?:(?:\d{1,2}:)?\d{1,2}:\d{2}|\d+(?:\.\d+)?\s*(?:min|mins|minutes|h|hr|hrs|hours))(?:\s+for\s+(?:a\s+)?(?:5k|10k|half marathon|marathon|full marathon))?$",
    re.IGNORECASE,
)

TOTAL_STEPS = 5
STEP_META = [
    ("YOUR GOAL", "GOAL"),
    ("ABOUT YOU", "PROFILE"),
    ("EXPERIENCE", "EXPERIENCE"),
    ("SCHEDULE", "SCHEDULE"),
    ("HEALTH", "HEALTH"),
]

RACE_OPTIONS = [
    ("5K", "3.1 MI · 6-10 WKS", "Great first race or speed goal."),
    ("10K", "6.2 MI · 8-12 WKS", "Endurance with a touch of speed."),
    ("Half Marathon", "21.1 KM · 10-14 WKS", "The popular weekend distance."),
    ("Full Marathon", "42.2 KM · 14-20 WKS", "The big one. We'll pace you safely."),
]

FITNESS_OPTIONS = [
    ("NOVICE", "Beginner", "I rarely run."),
    ("INTER", "Intermediate", "I run occasionally."),
    ("ELITE", "Advanced", "I run regularly."),
]


def _parse_number(raw: str, label: str, minimum: float, maximum: float) -> tuple[float | None, str | None]:
    try:
        value = float(raw)
    except ValueError:
        return None, f"Enter a valid {label}."
    if value < minimum or value > maximum:
        return None, f"{label.capitalize()} must be between {minimum:g} and {maximum:g}."
    return value, None


def _validate_recent_race_time(raw: str) -> tuple[str | None, str | None]:
    value = raw.strip()
    if not value:
        return None, None
    if RECENT_RACE_TIME_PATTERN.match(value):
        return value, None
    return None, "Recent race time must look like 25:30, 1:45:20, 5K 25:30, or 45 min."


def _set_step(step: int) -> None:
    st.session_state.ob_step = max(1, min(TOTAL_STEPS, step))
    st.rerun()


def _previous_step(step: int) -> None:
    _set_step(step - 1)


def _next_step(user, step: int) -> None:
    if step == TOTAL_STEPS:
        _save_onboarding(user)
        return

    step_errors = _validate_step(step)
    if step_errors:
        st.session_state.ob_errors = step_errors
        st.rerun()
    else:
        _set_step(step + 1)


def _render_step_nav(user, step: int) -> None:
    if step > 1:
        with st.container(key="ob_nav_back"):
            if st.button("\u2190", key=f"ob_nav_back_btn_{step}", help="Back"):
                _previous_step(step)

    with st.container(key="ob_nav_next"):
        help_text = "Finish onboarding" if step == TOTAL_STEPS else "Next"
        if st.button("\u2192", key=f"ob_nav_next_btn_{step}", type="primary", help=help_text):
            _next_step(user, step)


def _validate_step(step: int) -> list[str]:
    errors: list[str] = []
    if step == 1:
        if st.session_state.get("ob_goal_distance") not in ONBOARDING_GOAL_OPTIONS:
            errors.append("Pick the race you're training for.")
        return errors

    if step == 2:
        age_raw = str(st.session_state.get("ob_age", "")).strip()
        weight_raw = str(st.session_state.get("ob_weight", "")).strip()
        if not age_raw:
            errors.append("Enter your age.")
        else:
            age_value, age_error = _parse_number(age_raw, "age", 10, 100)
            if age_value is None or not age_raw.isdigit():
                errors.append(age_error or "Age must be a whole number.")
        if not weight_raw:
            errors.append("Enter your weight in kg.")
        else:
            _, weight_error = _parse_number(weight_raw, "weight in KG", 30, 200)
            if weight_error:
                errors.append(weight_error)
        if st.session_state.get("ob_sex") not in ONBOARDING_SEX_OPTIONS:
            errors.append("Choose a sex option.")
        return errors

    if step == 3:
        if normalize_fitness_level(st.session_state.get("ob_fitness")) not in {"NOVICE", "INTER", "ELITE"}:
            errors.append("Choose your fitness level.")
        weekly_km_raw = str(st.session_state.get("ob_current_weekly_km", "")).strip()
        if not weekly_km_raw:
            errors.append("Enter your current weekly distance.")
        else:
            _, weekly_km_error = _parse_number(weekly_km_raw, "current weekly KM", 0, 300)
            if weekly_km_error:
                errors.append(weekly_km_error)
        recent_raw = str(st.session_state.get("ob_recent_race_time", "")).strip()
        if recent_raw:
            _, recent_error = _validate_recent_race_time(recent_raw)
            if recent_error:
                errors.append(recent_error)
        return errors

    if step == 4:
        valid_days = [day for day, _label in ONBOARDING_DAY_OPTIONS]
        training_days = st.session_state.get("ob_training_days", []) or []
        if not training_days:
            errors.append("Select at least one training day.")
        if st.session_state.get("ob_preferred_long_run_day") not in valid_days:
            errors.append("Choose a preferred long run day.")
        race_date = st.session_state.get("ob_goal_race_date")
        if not isinstance(race_date, date):
            errors.append("Choose a target race date.")
        elif race_date < date.today():
            errors.append("Target race date must be today or later.")
        return errors

    return errors


def _set_goal_distance(name: str) -> None:
    st.session_state.ob_goal_distance = name
    st.rerun()


def _set_fitness(level: str) -> None:
    st.session_state.ob_fitness = level
    st.rerun()


def show_onboarding() -> None:
    user = st.session_state.user
    profile = get_user_profile(user.uid)
    prime_onboarding_state(user.uid, profile)

    if "ob_step" not in st.session_state:
        st.session_state.ob_step = 1
    step = st.session_state.ob_step
    section_kicker, section_label = STEP_META[step - 1]
    progress_pct = (step / TOTAL_STEPS) * 100

    st.markdown('<div class="onboarding-page-bg"></div>', unsafe_allow_html=True)

    with st.container(key="ob_wizard"):
        st.markdown(
            """
            <div class="ob-brand">
                <span class="ob-brand-mark">↗</span>
                <span>PaceUp</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="ob-progress">
                <div class="ob-progress-meta">
                    <div class="ob-progress-step"><strong>{step}</strong> / {TOTAL_STEPS}</div>
                    <div class="ob-progress-label">{html.escape(section_label)}</div>
                </div>
                <div class="ob-progress-track">
                    <div class="ob-progress-fill" style="width:{progress_pct:.0f}%"></div>
                </div>
            </div>
            <div class="ob-kicker"><span></span> Step {step} — {html.escape(section_kicker)}</div>
            """,
            unsafe_allow_html=True,
        )

        if step == 1:
            _step_goal()
        elif step == 2:
            _step_about()
        elif step == 3:
            _step_experience()
        elif step == 4:
            _step_schedule()
        elif step == 5:
            _step_health()

        st.markdown('<div class="ob-error-slot">', unsafe_allow_html=True)
        for message in st.session_state.pop("ob_errors", []):
            st.markdown(
                f'<div class="flash flash-error">{html.escape(message)}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    _render_step_nav(user, step)


def _step_goal() -> None:
    st.markdown(
        """
        <h1 class="ob-headline">What race are you training for?</h1>
        <p class="ob-sub">PaceUp shapes the entire plan around your target distance. You can change this later.</p>
        """,
        unsafe_allow_html=True,
    )
    selected = st.session_state.get("ob_goal_distance", "Full Marathon")
    with st.container(key="ob_race_grid"):
        row1 = st.columns(2, gap="medium")
        row2 = st.columns(2, gap="medium")
        cells = [*row1, *row2]
        for (name, meta, desc), col in zip(RACE_OPTIONS, cells):
            with col:
                is_selected = selected == name
                marker = "✓" if is_selected else "○"
                label = (
                    f"**{name}**  {marker}\n\n"
                    f":gray[{meta}]\n\n"
                    f"{desc}"
                )
                if st.button(
                    label,
                    key=f"ob_race_{name}",
                    type="primary" if is_selected else "secondary",
                    use_container_width=True,
                ):
                    _set_goal_distance(name)


def _step_about() -> None:
    st.markdown(
        """
        <h1 class="ob-headline">Tell us about you.</h1>
        <p class="ob-sub">A few basics so we can shape paces and weekly load to your body.</p>
        """,
        unsafe_allow_html=True,
    )
    with st.container(key="ob_about_grid"):
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            st.markdown('<div class="ob-field-label">Age</div>', unsafe_allow_html=True)
            st.text_input("Age", placeholder="28", key="ob_age", label_visibility="collapsed")
        with c2:
            st.markdown('<div class="ob-field-label">Weight (kg)</div>', unsafe_allow_html=True)
            st.text_input("Weight", placeholder="72", key="ob_weight", label_visibility="collapsed")
        with c3:
            st.markdown('<div class="ob-field-label">Sex</div>', unsafe_allow_html=True)
            st.selectbox("Sex", ONBOARDING_SEX_OPTIONS, key="ob_sex", label_visibility="collapsed")


def _step_experience() -> None:
    st.markdown(
        """
        <h1 class="ob-headline">How experienced are you?</h1>
        <p class="ob-sub">This sets the starting volume and intensity of your plan.</p>
        """,
        unsafe_allow_html=True,
    )
    selected = normalize_fitness_level(st.session_state.get("ob_fitness", "NOVICE"))
    with st.container(key="ob_fit_grid"):
        cols = st.columns(3, gap="medium")
        for (level, title, desc), col in zip(FITNESS_OPTIONS, cols):
            with col:
                is_selected = selected == level
                marker = "✓" if is_selected else "○"
                label = f"**{title}**  {marker}\n\n{desc}"
                if st.button(
                    label,
                    key=f"ob_fit_{level}",
                    type="primary" if is_selected else "secondary",
                    use_container_width=True,
                ):
                    _set_fitness(level)

    st.markdown('<div class="ob-field-label" style="margin-top:1.5rem;">Current weekly distance (km)</div>', unsafe_allow_html=True)
    st.text_input("Weekly km", placeholder="25", key="ob_current_weekly_km", label_visibility="collapsed")

    st.markdown('<div class="ob-field-label">Recent race time (optional)</div>', unsafe_allow_html=True)
    st.text_input(
        "Recent race time",
        placeholder="e.g. 25:30 for a 5K",
        key="ob_recent_race_time",
        label_visibility="collapsed",
    )


def _step_schedule() -> None:
    st.markdown(
        """
        <h1 class="ob-headline">When do you train?</h1>
        <p class="ob-sub">Pick the days you can run. We'll plan long runs around your preferred day.</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="ob-field-label">Training days</div>', unsafe_allow_html=True)
    with st.container(key="ob_days"):
        cols = st.columns(7, gap="small")
        for (day_name, short_label), col in zip(ONBOARDING_DAY_OPTIONS, cols):
            with col:
                if st.button(
                    short_label,
                    key=f"ob_day_{day_name}",
                    type="primary" if day_name in st.session_state.ob_training_days else "secondary",
                    use_container_width=True,
                ):
                    toggle_training_day(day_name)
                    st.rerun()

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown('<div class="ob-field-label">Preferred long run day</div>', unsafe_allow_html=True)
        st.selectbox(
            "Long run day",
            [day for day, _label in ONBOARDING_DAY_OPTIONS],
            key="ob_preferred_long_run_day",
            label_visibility="collapsed",
        )
    with c2:
        st.markdown('<div class="ob-field-label">Target race date</div>', unsafe_allow_html=True)
        if isinstance(st.session_state.get("ob_goal_race_date"), date) and st.session_state.ob_goal_race_date < date.today():
            st.session_state.ob_goal_race_date = None
        st.date_input(
            "Race date",
            key="ob_goal_race_date",
            min_value=date.today(),
            label_visibility="collapsed",
        )


def _step_health() -> None:
    st.markdown(
        """
        <h1 class="ob-headline">Anything we should know?</h1>
        <p class="ob-sub">PaceUp will adapt the plan if you flag a current injury or limitation.</p>
        """,
        unsafe_allow_html=True,
    )
    st.checkbox(
        "I currently have an injury or physical limitation.",
        key="ob_injury_flag",
    )
    st.markdown(
        '<p class="ob-disclaimer">PaceUp is not a medical advisor. For pain, injury, or medical concerns, check with a qualified professional.</p>',
        unsafe_allow_html=True,
    )


def _save_onboarding(user) -> None:
    errors: list[str] = []
    age_raw = str(st.session_state.get("ob_age", "")).strip()
    weight_raw = str(st.session_state.get("ob_weight", "")).strip()
    weekly_km_raw = str(st.session_state.get("ob_current_weekly_km", "")).strip()
    recent_race_time_raw = str(st.session_state.get("ob_recent_race_time", "")).strip()
    training_days = st.session_state.get("ob_training_days", []) or []
    valid_days = [day for day, _label in ONBOARDING_DAY_OPTIONS]

    age_value, age_error = _parse_number(age_raw, "age", 10, 100)
    if age_value is not None and not age_raw.isdigit():
        age_value = None
        age_error = "Age must be a whole number."
    weight, weight_error = _parse_number(weight_raw, "weight in KG", 30, 200)
    current_weekly_km, weekly_km_error = _parse_number(weekly_km_raw or "0", "current weekly KM", 0, 300)
    recent_race_time, recent_race_time_error = _validate_recent_race_time(recent_race_time_raw)
    age = int(age_value) if age_value is not None else None

    for error in (age_error, weight_error, weekly_km_error, recent_race_time_error):
        if error:
            errors.append(error)

    if not training_days:
        errors.append("Select at least one training day.")
    if st.session_state.get("ob_sex") not in ONBOARDING_SEX_OPTIONS:
        errors.append("Choose a valid sex option.")
    if st.session_state.get("ob_goal_distance") not in ONBOARDING_GOAL_OPTIONS:
        errors.append("Choose a valid goal distance.")
    if st.session_state.get("ob_preferred_long_run_day") not in valid_days:
        errors.append("Choose a valid preferred long run day.")
    if not isinstance(st.session_state.get("ob_goal_race_date"), date):
        errors.append("Choose a valid target race date.")
    elif st.session_state.ob_goal_race_date < date.today():
        errors.append("Target race date must be today or later.")

    if errors:
        log_event(user.uid, "onboarding_validation_failed", {"errors": errors})
        st.session_state.ob_errors = errors
        st.rerun()
        return

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
                "recent_race_time": recent_race_time,
                "training_days_per_week": len(training_days),
                "training_days": training_days,
                "preferred_long_run_day": st.session_state.ob_preferred_long_run_day,
                "injury_flag": bool(st.session_state.get("ob_injury_flag", False)),
            },
        )
        st.session_state.user_profile = build_chat_profile(user)
        st.session_state.user_profile_uid = user.uid
        st.session_state.onboarding_completed = True
        st.session_state.show_name_prompt_after_onboarding = True
        st.session_state.ob_step = 1
        log_event(user.uid, "onboarding_completed", {"training_days_per_week": len(training_days)})
        go_to("chat")
    except Exception as exc:
        st.session_state.ob_errors = [f"Failed to save profile: {exc}"]
        st.rerun()
