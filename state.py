from __future__ import annotations

import html
import json
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

import config
from config import ONBOARDING_DAY_OPTIONS, ONBOARDING_SEX_OPTIONS, normalize_fitness_level, normalize_goal_distance
from services import firebase as firebase_service


VALID_PAGES = {"home", "login", "register", "about", "contact", "onboarding", "chat"}
DEFAULT_PAGE = "home"
PAGE_QUERY_PARAM = "page"
AUTH_COOKIE_NAME = getattr(firebase_service, "AUTH_COOKIE_NAME", "paceup_refresh_token")
check_onboarding_status = firebase_service.check_onboarding_status
clear_auth_session = firebase_service.clear_auth_session
firebase_restore_saved_session = firebase_service.restore_saved_session


def _auth_cookie_secure() -> bool:
    configured = getattr(config, "AUTH_COOKIE_SECURE", None)
    if configured is not None:
        return str(configured).strip().lower() in {"1", "true", "yes", "on"}
    get_secret = getattr(config, "get_secret", None)
    raw_value = get_secret("AUTH_COOKIE_SECURE", "") if callable(get_secret) else ""
    return str(raw_value).strip().lower() in {"1", "true", "yes", "on"}


AUTH_COOKIE_SECURE = _auth_cookie_secure()


def _get_query_page() -> str | None:
    page = st.query_params.get(PAGE_QUERY_PARAM)
    if isinstance(page, list):
        page = page[0] if page else None
    return page if isinstance(page, str) and page in VALID_PAGES else None


def _set_page_query(page: str) -> None:
    if page in VALID_PAGES and st.query_params.get(PAGE_QUERY_PARAM) != page:
        st.query_params[PAGE_QUERY_PARAM] = page


def init_state() -> None:
    defaults = {
        "page": "home",
        "theme": "light",
        "user": None,
        "signed_out": False,
        "flash": None,
        "auth_restore_attempted": False,
        "auth_restore_attempts": 0,
        "auth_bridge_ready": True,
        "pending_auth_token": "",
        "login_email": "",
        "login_password": "",
        "clear_login_password_pending": False,
        "reg_name": "",
        "reg_email": "",
        "reg_pass": "",
        "reg_confirm": "",
        "clear_register_pending": False,
        "chat_sessions": [],
        "active_chat_id": None,
        "active_session_id": None,
        "messages": [],
        "messages_cursor": None,
        "chat_has_more_messages": False,
        "pending_assistant_session_id": None,
        "pending_assistant_messages": [],
        "user_profile": {},
        "user_profile_uid": None,
        "ob_fitness": "NOVICE",
        "ob_state_uid": None,
        "ob_training_days": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    query_page = _get_query_page()
    if query_page:
        st.session_state.page = query_page
    elif st.session_state.get("page") not in VALID_PAGES:
        st.session_state.page = DEFAULT_PAGE
    else:
        # A browser Back navigation can land on the bare app URL with no
        # query params. Treat that URL as the public landing page.
        st.session_state.page = DEFAULT_PAGE


def sync_page_to_url() -> None:
    current = st.session_state.get("page")
    if current:
        _set_page_query(current)


def route_href(page: str) -> str:
    safe_page = page if page in VALID_PAGES else DEFAULT_PAGE
    return f"?{PAGE_QUERY_PARAM}={safe_page}"


def route_link(label: str, page: str, css_class: str) -> None:
    st.markdown(
        f'<a class="{css_class}" href="{route_href(page)}" target="_self">{html.escape(label)}</a>',
        unsafe_allow_html=True,
    )


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
    st.session_state.page = page if page in VALID_PAGES else DEFAULT_PAGE
    _set_page_query(st.session_state.page)
    st.rerun()


def toggle_theme() -> None:
    st.session_state.theme = "dark" if st.session_state.get("theme", "light") == "light" else "light"
    st.rerun()


def get_home_page() -> str:
    if st.session_state.user:
        if st.session_state.page == "onboarding" or not check_onboarding_status(st.session_state.user.uid):
            return "onboarding"
        return "chat"
    return "home"


def restore_saved_session() -> None:
    firebase_restore_saved_session()


def logout_user() -> None:
    user = st.session_state.get("user")
    secure_cookie = "; Secure" if AUTH_COOKIE_SECURE else ""
    st.session_state.signed_out = True
    clear_auth_session(user.uid if user else None)
    st.session_state.user = None
    st.session_state.page = "login"
    _set_page_query("login")
    st.session_state.auth_restore_attempted = False
    st.session_state.auth_restore_attempts = 0
    st.session_state.clear_login_password_pending = True
    st.session_state.messages = []
    st.session_state.chat_sessions = []
    st.session_state.active_chat_id = None
    st.session_state.active_session_id = None
    st.session_state.messages_cursor = None
    st.session_state.chat_has_more_messages = False
    st.session_state.pending_assistant_session_id = None
    st.session_state.pending_assistant_messages = []
    st.session_state.user_profile = {}
    st.session_state.user_profile_uid = None
    st.session_state.onboarding_completed = False
    set_flash("success", "Signed out.")
    components.html(
        f"""
        <script>
            try {{ window.localStorage.removeItem({json.dumps(AUTH_COOKIE_NAME)}); }} catch (e) {{}}
            try {{ window.sessionStorage.removeItem({json.dumps(AUTH_COOKIE_NAME + "_restore_attempted")}); }} catch (e) {{}}
            document.cookie = {json.dumps(f"{AUTH_COOKIE_NAME}=; Max-Age=0; Path=/; SameSite=Lax")};
            document.cookie = {json.dumps(f"{AUTH_COOKIE_NAME}=; Max-Age=0; Path=/; SameSite=Lax{secure_cookie}")};
            setTimeout(function () {{
                window.parent.location.href = {json.dumps(route_href("login"))};
            }}, 350);
        </script>
        """,
        height=0,
    )
    st.stop()


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
