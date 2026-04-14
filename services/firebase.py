from __future__ import annotations

import json
from datetime import datetime, timezone

import firebase_admin
import requests
import streamlit as st
from firebase_admin import auth, credentials, firestore
try:
    from streamlit_cookies_controller import CookieController
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without the extra package
    CookieController = None

from config import BASE_DIR, FIREBASE_WEB_API_KEY

AUTH_COOKIE_NAME = "paceup_refresh_token"
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24 * 30


def _firebase_credentials_payload() -> dict:
    try:
        if "firebase" in st.secrets:
            payload = dict(st.secrets["firebase"])
            private_key = payload.get("private_key")
            if isinstance(private_key, str):
                payload["private_key"] = private_key.replace("\\n", "\n")
            return payload
    except Exception:
        pass

    config_path = BASE_DIR / "firebase_config.json"
    if not config_path.exists():
        raise FileNotFoundError(
            "Firebase credentials not found. Provide st.secrets['firebase'] in deployment or firebase_config.json locally."
        )

    payload = json.loads(config_path.read_text(encoding="utf-8"))
    private_key = payload.get("private_key")
    if isinstance(private_key, str):
        payload["private_key"] = private_key.replace("\\n", "\n")
    return payload


def init_firebase() -> None:
    if not firebase_admin._apps:
        cred = credentials.Certificate(_firebase_credentials_payload())
        firebase_admin.initialize_app(cred)


def _cookie_controller() -> CookieController:
    if CookieController is None:
        return None
    return CookieController(key="paceup_auth_cookies")


def _get_refresh_token_cookie() -> str:
    controller = _cookie_controller()
    if controller is None:
        return ""
    token = controller.get(AUTH_COOKIE_NAME)
    return str(token) if token else ""


def _set_refresh_token_cookie(refresh_token: str) -> None:
    if not refresh_token:
        return
    controller = _cookie_controller()
    if controller is None:
        return
    controller.set(
        AUTH_COOKIE_NAME,
        refresh_token,
        path="/",
        max_age=AUTH_COOKIE_MAX_AGE,
        same_site="lax",
    )


def clear_auth_session() -> None:
    controller = _cookie_controller()
    if controller is None:
        return
    controller.remove(AUTH_COOKIE_NAME, path="/", same_site="lax")


def register_user(email: str, password: str, full_name: str):
    normalized_email = email.strip()
    normalized_name = full_name.strip()
    user = None
    try:
        user = auth.create_user(
            email=normalized_email,
            password=password,
            display_name=normalized_name,
        )
        create_user_profile(user, normalized_name)
        return user, None
    except Exception as exc:
        if user is not None:
            try:
                auth.delete_user(user.uid)
            except Exception as cleanup_exc:
                return None, f"{exc} Cleanup failed: {cleanup_exc}"
        return None, str(exc)


def create_user_profile(user: auth.UserRecord, full_name: str) -> None:
    now = datetime.now(timezone.utc)
    firestore.client().collection("users").document(user.uid).set(
        {
            "uid": user.uid,
            "email": user.email or "",
            "full_name": full_name,
            "display_name": user.display_name or full_name,
            "onboarding_completed": False,
            "fitness_level": None,
            "goal_distance": None,
            "goal_race_date": None,
            "training_days_per_week": None,
            "current_weekly_km": None,
            "recent_race_time": None,
            "preferred_long_run_day": None,
            "injury_flag": False,
            "active_plan_id": None,
            "created_at": now,
            "updated_at": now,
        }
    )


def login_user(email: str, password: str):
    if not FIREBASE_WEB_API_KEY:
        return None, "Missing FIREBASE_WEB_API_KEY."
    url = (
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        f"?key={FIREBASE_WEB_API_KEY}"
    )
    try:
        response = requests.post(
            url,
            json={
                "email": email.strip(),
                "password": password,
                "returnSecureToken": True,
            },
            timeout=15,
        )
        data = response.json()
        if response.status_code != 200:
            return None, data.get("error", {}).get("message", "Login failed.")
        user = auth.get_user_by_email(email.strip())
        _set_refresh_token_cookie(data.get("refreshToken", ""))
        return user, None
    except Exception as exc:
        return None, str(exc)


def restore_saved_session() -> None:
    if st.session_state.get("user") is not None:
        return

    refresh_token = _get_refresh_token_cookie()
    if not FIREBASE_WEB_API_KEY or not refresh_token:
        return

    url = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_WEB_API_KEY}"
    try:
        response = requests.post(
            url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            timeout=15,
        )
        data = response.json()
    except Exception:
        return

    if response.status_code != 200:
        clear_auth_session()
        return

    uid = data.get("user_id")
    email = data.get("user_email")
    try:
        if uid:
            user = auth.get_user(uid)
        elif email:
            user = auth.get_user_by_email(email)
        else:
            clear_auth_session()
            return
    except Exception:
        clear_auth_session()
        return

    _set_refresh_token_cookie(data.get("refresh_token", refresh_token))
    st.session_state.user = user
    st.session_state.page = "chat" if check_onboarding_status(user.uid) else "onboarding"


def check_onboarding_status(uid: str) -> bool:
    try:
        doc = firestore.client().collection("users").document(uid).get()
        if doc.exists:
            return bool(doc.to_dict().get("onboarding_completed", False))
        return False
    except Exception:
        return False


def save_onboarding_data(uid: str, data: dict) -> None:
    data["onboarding_completed"] = True
    data["updated_at"] = datetime.now(timezone.utc)
    firestore.client().collection("users").document(uid).update(data)


def get_user_profile(uid: str) -> dict:
    try:
        doc = firestore.client().collection("users").document(uid).get()
        return doc.to_dict() if doc.exists else {}
    except Exception:
        return {}


def build_chat_profile(user: auth.UserRecord) -> dict:
    profile = get_user_profile(user.uid)
    display_name = (
        profile.get("display_name")
        or profile.get("full_name")
        or user.display_name
        or (user.email.split("@", 1)[0] if user.email else "Runner")
    )
    return {
        "uid": user.uid,
        "email": user.email or profile.get("email", ""),
        "display_name": display_name,
        "full_name": profile.get("full_name") or display_name,
        "age": profile.get("age"),
        "weight_kg": profile.get("weight_kg"),
        "sex": profile.get("sex"),
        "fitness_level": profile.get("fitness_level"),
        "goal_distance": profile.get("goal_distance"),
        "goal_race_date": profile.get("goal_race_date"),
        "current_weekly_km": profile.get("current_weekly_km"),
        "training_days_per_week": profile.get("training_days_per_week"),
        "training_days": profile.get("training_days") or [],
        "preferred_long_run_day": profile.get("preferred_long_run_day"),
        "recent_race_time": profile.get("recent_race_time"),
        "injury_flag": bool(profile.get("injury_flag", False)),
        "onboarding_completed": bool(profile.get("onboarding_completed", False)),
        "active_plan_id": profile.get("active_plan_id"),
    }
