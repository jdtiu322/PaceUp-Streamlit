from __future__ import annotations

import html
from datetime import datetime

import streamlit as st

from config import ONBOARDING_DAY_OPTIONS, ONBOARDING_SEX_OPTIONS, normalize_fitness_level, normalize_goal_distance
from services.firebase import check_onboarding_status, clear_auth_session, restore_saved_session as firebase_restore_saved_session


def init_state() -> None:
    defaults = {
        "page": "login",
        "user": None,
        "flash": None,
        "auth_restore_attempted": False,
        "login_email": "",
        "login_password": "",
        "clear_login_password_pending": False,
        "reg_name": "",
        "reg_email": "",
        "reg_pass": "",
        "reg_confirm": "",
        "clear_register_pending": False,
        "chat_sessions": [],
        "active_session_id": None,
        "messages": [],
        "user_profile": {},
        "ob_fitness": "NOVICE",
        "ob_state_uid": None,
        "ob_training_days": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_flash(kind: str, message: str) -> None:
    st.session_state.flash = {"kind": kind, "message": message}


def show_flash() -> None:
    flash = st.session_state.pop("flash", None)
    if not flash:
        return
    st.markdown(
        f'<div class="flash flash-{flash["kind"]}">{html.escape(flash["message"])}</div>',
        unsafe_allow_html=True,
    )


def go_to(page: str) -> None:
    st.session_state.page = page
    st.rerun()


def get_home_page() -> str:
    if st.session_state.user:
        if st.session_state.page == "onboarding" or not check_onboarding_status(st.session_state.user.uid):
            return "onboarding"
        return "chat"
    return "login"


def restore_saved_session() -> None:
    firebase_restore_saved_session()


def logout_user() -> None:
    clear_auth_session()
    st.session_state.user = None
    st.session_state.page = "login"
    st.session_state.clear_login_password_pending = True
    st.session_state.messages = []
    st.session_state.chat_sessions = []
    st.session_state.active_session_id = None
    st.session_state.user_profile = {}
    set_flash("success", "Signed out.")
    st.rerun()


def clear_register() -> None:
    for key in ("reg_name", "reg_email", "reg_pass", "reg_confirm"):
        st.session_state[key] = ""


def toggle_training_day(day: str) -> None:
    selected_days = list(st.session_state.get("ob_training_days", []))
    if day in selected_days:
        selected_days = [item for item in selected_days if item != day]
    else:
        selected_days.append(day)
    st.session_state.ob_training_days = [item for item, _label in ONBOARDING_DAY_OPTIONS if item in selected_days]


def prime_onboarding_state(uid: str, profile: dict) -> None:
    if st.session_state.get("ob_state_uid") == uid:
        st.session_state.ob_fitness = normalize_fitness_level(st.session_state.get("ob_fitness"))
        st.session_state.ob_goal_distance = normalize_goal_distance(st.session_state.get("ob_goal_distance"))
        st.session_state.ob_age = str(st.session_state.get("ob_age", ""))
        st.session_state.ob_weight = str(st.session_state.get("ob_weight", ""))
        st.session_state.ob_current_weekly_km = str(st.session_state.get("ob_current_weekly_km", ""))
        st.session_state.ob_recent_race_time = str(st.session_state.get("ob_recent_race_time", ""))
        goal_date = st.session_state.get("ob_goal_race_date")
        if isinstance(goal_date, str):
            try:
                st.session_state.ob_goal_race_date = datetime.fromisoformat(goal_date).date()
            except Exception:
                st.session_state.ob_goal_race_date = datetime.now().date()
        st.session_state.ob_training_days = [
            day for day, _label in ONBOARDING_DAY_OPTIONS if day in st.session_state.get("ob_training_days", [])
        ]
        return

    race_date_raw = profile.get("goal_race_date")
    try:
        race_date = datetime.fromisoformat(race_date_raw).date() if race_date_raw else datetime.now().date()
    except Exception:
        race_date = datetime.now().date()

    training_days = profile.get("training_days") or []
    defaults = {
        "ob_state_uid": uid,
        "ob_age": str(profile.get("age") or ""),
        "ob_weight": str(profile.get("weight_kg") or ""),
        "ob_sex": profile.get("sex") or ONBOARDING_SEX_OPTIONS[0],
        "ob_fitness": normalize_fitness_level(profile.get("fitness_level")),
        "ob_goal_distance": normalize_goal_distance(profile.get("goal_distance")),
        "ob_goal_race_date": race_date,
        "ob_current_weekly_km": str(profile.get("current_weekly_km") or ""),
        "ob_recent_race_time": profile.get("recent_race_time") or "",
        "ob_training_days": [day for day, _label in ONBOARDING_DAY_OPTIONS if day in training_days],
        "ob_preferred_long_run_day": profile.get("preferred_long_run_day") or "Sunday",
        "ob_injury_flag": bool(profile.get("injury_flag", False)),
    }
    for key, value in defaults.items():
        st.session_state[key] = value
