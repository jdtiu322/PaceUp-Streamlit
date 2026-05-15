from __future__ import annotations

import json
import logging
from datetime import date, datetime, timedelta, timezone

import firebase_admin
import requests
import streamlit as st
import streamlit.components.v1 as st_components
from firebase_admin import auth, credentials, firestore
try:
    from streamlit_cookies_controller import CookieController
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without the extra package
    CookieController = None

import config

BASE_DIR = config.BASE_DIR
FIREBASE_WEB_API_KEY = config.FIREBASE_WEB_API_KEY


def _auth_cookie_secure() -> bool:
    configured = getattr(config, "AUTH_COOKIE_SECURE", None)
    if configured is not None:
        return str(configured).strip().lower() in {"1", "true", "yes", "on"}
    get_secret = getattr(config, "get_secret", None)
    raw_value = get_secret("AUTH_COOKIE_SECURE", "") if callable(get_secret) else ""
    return str(raw_value).strip().lower() in {"1", "true", "yes", "on"}


AUTH_COOKIE_SECURE = _auth_cookie_secure()

AUTH_COOKIE_NAME = "paceup_refresh_token"
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24 * 30
AUTH_SESSION_QUERY_PARAM = "_auth"
logger = logging.getLogger(__name__)
_AUTH_BRIDGE = st_components.declare_component(
    "paceup_auth_bridge",
    path=str(BASE_DIR / "services" / "auth_bridge_component"),
)


def _coerce_iso_date(value) -> str | None:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            return date.fromisoformat(text[:10]).isoformat()
        except ValueError:
            return None
    return None


def _firebase_credentials_payload() -> dict:
    try:
        if "firebase" in st.secrets:
            payload = dict(st.secrets["firebase"])
            private_key = payload.get("private_key")
            if isinstance(private_key, str):
                payload["private_key"] = private_key.replace("\\n", "\n")
            return payload
    except Exception:
        logger.exception("Failed to read Firebase credentials from Streamlit secrets.")

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
    try:
        firebase_admin.get_app()
        return
    except ValueError:
        pass

    cred = credentials.Certificate(_firebase_credentials_payload())
    try:
        firebase_admin.initialize_app(cred)
    except ValueError as exc:
        if "already exists" not in str(exc):
            raise
        logger.warning("Firebase default app was initialized during startup; reusing it.")


@st.cache_resource(show_spinner=False)
def get_firestore_client():
    return firestore.client()


_COOKIE_CONTROLLER_CACHE_KEY = "_paceup_cookie_controller"


def _cookie_controller() -> CookieController:
    if CookieController is None:
        return None
    cached = st.session_state.get(_COOKIE_CONTROLLER_CACHE_KEY)
    if cached is not None:
        return cached
    controller = CookieController(key="paceup_auth_cookies")
    st.session_state[_COOKIE_CONTROLLER_CACHE_KEY] = controller
    return controller


def _read_cookie_from_context(name: str) -> str:
    """Read a cookie from the inbound request synchronously, before the async controller mounts."""
    try:
        cookies = st.context.cookies  # type: ignore[attr-defined]
        if cookies:
            value = cookies.get(name)
            if value:
                from urllib.parse import unquote
                return unquote(str(value))
    except Exception:
        pass
    try:
        headers = st.context.headers  # type: ignore[attr-defined]
        if headers:
            cookie_header = headers.get("Cookie") or headers.get("cookie") or ""
            if cookie_header:
                from urllib.parse import unquote
                for pair in cookie_header.split(";"):
                    if "=" in pair:
                        n, _, v = pair.strip().partition("=")
                        if n == name:
                            return unquote(v)
    except Exception:
        pass
    return ""


def _get_url_auth_token() -> str:
    """One-shot bridge: the recovery JS adds ?_auth=<token> to the URL when the cookie can't be delivered."""
    try:
        token = st.query_params.get(AUTH_SESSION_QUERY_PARAM)
        if isinstance(token, list):
            token = token[0] if token else None
        return str(token) if token else ""
    except Exception:
        return ""


def _clear_url_auth_token() -> None:
    try:
        if AUTH_SESSION_QUERY_PARAM in st.query_params:
            st.query_params.pop(AUTH_SESSION_QUERY_PARAM, None)
    except Exception:
        try:
            del st.query_params[AUTH_SESSION_QUERY_PARAM]
        except Exception:
            pass


def _auth_bridge(method: str, *, token: str = "", key: str) -> dict:
    try:
        value = _AUTH_BRIDGE(
            method=method,
            name=AUTH_COOKIE_NAME,
            token=token,
            maxAge=AUTH_COOKIE_MAX_AGE,
            secure=AUTH_COOKIE_SECURE,
            default={"ready": False, "token": ""},
            key=key,
        )
    except Exception:
        logger.exception("Browser auth bridge failed during %s.", method)
        st.session_state.auth_bridge_ready = True
        return {}

    return value if isinstance(value, dict) else {}


def _get_auth_bridge_token() -> str:
    value = _auth_bridge("get", key="paceup_auth_bridge_get")
    ready = bool(value.get("ready"))
    st.session_state.auth_bridge_ready = ready
    if not ready:
        return ""
    token = value.get("token")
    return str(token) if token else ""


def _set_auth_bridge_token(refresh_token: str) -> None:
    if refresh_token:
        _auth_bridge("set", token=refresh_token, key="paceup_auth_bridge_set")
        st.session_state.auth_bridge_ready = True


def _clear_auth_bridge_token() -> None:
    _auth_bridge("clear", key="paceup_auth_bridge_clear")
    st.session_state.auth_bridge_ready = True


def create_auth_session(refresh_token: str, uid: str | None = None) -> str:
    """Returns the refresh token directly so callers can stuff it into the URL bridge."""
    return refresh_token


def persist_auth_session(refresh_token: str) -> None:
    """Best-effort browser persistence for the Firebase refresh token."""
    try:
        _set_refresh_token_cookie(refresh_token)
    except Exception:
        logger.exception("Failed to persist Firebase auth refresh token.")


def _get_refresh_token_cookie(*, use_browser_bridge: bool = True) -> str:
    sync_value = _read_cookie_from_context(AUTH_COOKIE_NAME)
    if sync_value:
        st.session_state.auth_bridge_ready = True
        return sync_value
    bridge_value = _get_url_auth_token()
    if bridge_value:
        st.session_state.auth_bridge_ready = True
        return bridge_value
    if not use_browser_bridge:
        return ""
    browser_value = _get_auth_bridge_token()
    if browser_value:
        return browser_value
    controller = _cookie_controller()
    if controller is None:
        return ""
    token = controller.get(AUTH_COOKIE_NAME)
    if token:
        st.session_state.auth_bridge_ready = True
        return str(token)
    return ""


def refresh_auth_cookie_cache() -> None:
    if _COOKIE_CONTROLLER_CACHE_KEY not in st.session_state:
        return
    controller = _cookie_controller()
    if controller is None:
        return
    try:
        controller.refresh()
    except Exception:
        logger.exception("Failed to refresh browser auth cookie cache.")


def _expire_cookie(controller: CookieController, name: str, *, secure: bool) -> None:
    controller.set(
        name,
        "",
        path="/",
        expires=datetime.now() - timedelta(days=1),
        max_age=0,
        secure=secure,
        same_site="lax",
    )
    try:
        controller.remove(name, path="/", secure=secure, same_site="lax")
    except Exception:
        # Some controller versions raise if the cached cookie snapshot does not
        # contain the cookie. The explicit expired set above still clears it.
        logger.debug("Cookie %s was not present in the controller cache.", name, exc_info=True)


def _set_refresh_token_cookie(refresh_token: str) -> None:
    if not refresh_token:
        return
    _set_auth_bridge_token(refresh_token)
    controller = _cookie_controller()
    if controller is None:
        return
    controller.set(
        AUTH_COOKIE_NAME,
        refresh_token,
        path="/",
        max_age=AUTH_COOKIE_MAX_AGE,
        secure=AUTH_COOKIE_SECURE,
        same_site="lax",
    )


def clear_auth_session(user_uid: str | None = None) -> None:
    if user_uid:
        try:
            auth.revoke_refresh_tokens(user_uid)
        except Exception:
            logger.exception("Failed to revoke Firebase refresh tokens for user %s.", user_uid)

    controller = _cookie_controller()
    _clear_auth_bridge_token()
    if controller is None:
        return
    try:
        _expire_cookie(controller, AUTH_COOKIE_NAME, secure=AUTH_COOKIE_SECURE)
        _expire_cookie(controller, AUTH_COOKIE_NAME, secure=not AUTH_COOKIE_SECURE)
    except Exception:
        logger.exception("Failed to clear auth refresh-token cookie.")


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
        logger.exception("Registration failed for %s.", normalized_email)
        if user is not None:
            try:
                auth.delete_user(user.uid)
            except Exception as cleanup_exc:
                logger.exception("Failed to clean up Auth user %s after profile creation failure.", user.uid)
                return None, f"{exc} Cleanup failed: {cleanup_exc}"
        return None, str(exc)


def create_user_profile(user: auth.UserRecord, full_name: str) -> None:
    now = datetime.now(timezone.utc)
    get_firestore_client().collection("users").document(user.uid).set(
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


def ensure_user_profile(user: auth.UserRecord) -> dict:
    db = get_firestore_client()
    ref = db.collection("users").document(user.uid)
    doc = ref.get()
    if doc.exists:
        return doc.to_dict() or {}

    now = datetime.now(timezone.utc)
    display_name = user.display_name or (user.email.split("@", 1)[0] if user.email else "Runner")
    profile = {
        "uid": user.uid,
        "email": user.email or "",
        "full_name": display_name,
        "display_name": display_name,
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
    ref.set(profile)
    logger.warning("Bootstrapped missing Firestore profile for Auth user %s.", user.uid)
    return profile


def login_user(email: str, password: str):
    if not FIREBASE_WEB_API_KEY:
        return None, "Missing FIREBASE_WEB_API_KEY.", ""
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
            return None, data.get("error", {}).get("message", "Login failed."), ""
        refresh_token = data.get("refreshToken", "")
        user = auth.get_user_by_email(email.strip())
        ensure_user_profile(user)
        return user, None, refresh_token
    except Exception as exc:
        logger.exception("Login failed for %s.", email.strip())
        return None, str(exc), ""


def restore_saved_session() -> None:
    refresh_auth_cookie_cache()

    if st.session_state.get("signed_out"):
        st.session_state.signed_out = True
        return

    if st.session_state.get("user") is not None:
        return

    refresh_token = _get_refresh_token_cookie(use_browser_bridge=True)
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
        logger.exception("Failed to refresh saved Firebase auth session.")
        return

    if response.status_code != 200:
        clear_auth_session()
        return

    id_token = data.get("id_token")
    if not id_token:
        clear_auth_session()
        return

    try:
        decoded_token = auth.verify_id_token(id_token, check_revoked=True)
    except (auth.RevokedIdTokenError, auth.ExpiredIdTokenError, auth.InvalidIdTokenError):
        logger.info("Saved Firebase auth session is no longer valid; clearing local session.")
        clear_auth_session()
        return
    except auth.UserDisabledError:
        logger.warning("Saved Firebase auth session belongs to a disabled user; clearing local session.")
        clear_auth_session()
        return
    except Exception:
        logger.exception("Unexpected error while validating saved Firebase auth session.")
        return

    uid = data.get("user_id")
    email = data.get("user_email")
    verified_uid = decoded_token.get("uid")
    if verified_uid and uid and verified_uid != uid:
        logger.warning("Saved Firebase auth session UID mismatch: token=%s response=%s.", verified_uid, uid)
        clear_auth_session()
        return

    try:
        if verified_uid:
            user = auth.get_user(verified_uid)
        elif uid:
            user = auth.get_user(uid)
        elif email:
            user = auth.get_user_by_email(email)
        else:
            clear_auth_session()
            return
    except Exception:
        logger.exception("Failed to load Firebase Auth user during session restore.")
        clear_auth_session()
        return

    try:
        ensure_user_profile(user)
    except Exception:
        logger.exception("Failed to ensure Firestore profile during session restore.")
        clear_auth_session()
        return

    next_refresh_token = data.get("refresh_token", refresh_token)
    _set_refresh_token_cookie(next_refresh_token)
    _clear_url_auth_token()
    st.session_state.user = user
    st.session_state.signed_out = False
    st.session_state.auth_bridge_ready = True
    st.session_state.auth_restore_attempted = False
    st.session_state.auth_restore_attempts = 0

    onboarding_done = check_onboarding_status(user.uid)
    st.session_state.onboarding_completed = onboarding_done
    current_page = st.session_state.get("page")
    if not onboarding_done:
        # Force incomplete users into onboarding regardless of where they landed.
        st.session_state.page = "onboarding"
    elif current_page in {"home", "login", "register", None}:
        # Completed user landed on a public page — send them into the app.
        st.session_state.page = "chat"
    # else: respect the current page (onboarding/chat/about/contact)


def check_onboarding_status(uid: str) -> bool:
    try:
        doc = get_firestore_client().collection("users").document(uid).get()
        if doc.exists:
            return bool(doc.to_dict().get("onboarding_completed", False))
        return False
    except Exception:
        logger.exception("Failed to check onboarding status for user %s.", uid)
        return False


def save_onboarding_data(uid: str, data: dict) -> None:
    db = get_firestore_client()
    user_ref = db.collection("users").document(uid)
    current_profile = {}
    try:
        current_doc = user_ref.get()
        current_profile = current_doc.to_dict() if current_doc.exists else {}
    except Exception:
        logger.exception("Failed to read existing profile before onboarding save for user %s.", uid)

    normalized_goal_date = _coerce_iso_date(data.get("goal_race_date"))
    if normalized_goal_date:
        data["goal_race_date"] = normalized_goal_date
    data["onboarding_completed"] = True
    data["preferred_name_prompted"] = False
    data["updated_at"] = datetime.now(timezone.utc)
    user_ref.update(data)

    active_plan_id = str(current_profile.get("active_plan_id") or "").strip()
    if active_plan_id and normalized_goal_date:
        try:
            user_ref.collection("plans").document(active_plan_id).update(
                {
                    "goal_distance": data.get("goal_distance"),
                    "goal_race_date": normalized_goal_date,
                    "preferred_long_run_day": data.get("preferred_long_run_day"),
                    "updated_at": data["updated_at"],
                }
            )
        except Exception:
            logger.exception("Failed to sync onboarding goal date to active plan for user %s.", uid)


def update_goal_race_date(uid: str, goal_race_date) -> str:
    normalized_goal_date = _coerce_iso_date(goal_race_date)
    if not normalized_goal_date:
        raise ValueError("Choose a valid target race date.")

    now = datetime.now(timezone.utc)
    db = get_firestore_client()
    user_ref = db.collection("users").document(uid)
    profile_doc = user_ref.get()
    profile = profile_doc.to_dict() if profile_doc.exists else {}
    user_ref.update({"goal_race_date": normalized_goal_date, "updated_at": now})

    active_plan_id = str(profile.get("active_plan_id") or "").strip()
    if active_plan_id:
        try:
            user_ref.collection("plans").document(active_plan_id).update(
                {"goal_race_date": normalized_goal_date, "updated_at": now}
            )
        except Exception:
            logger.exception("Failed to sync chat-updated goal date to active plan for user %s.", uid)
    return normalized_goal_date


def save_preferred_name(uid: str, preferred_name: str) -> str:
    name = " ".join((preferred_name or "").split())[:80]
    if not name:
        return ""

    now = datetime.now(timezone.utc)
    get_firestore_client().collection("users").document(uid).update(
        {
            "display_name": name,
            "preferred_name": name,
            "preferred_name_prompted": True,
            "updated_at": now,
        }
    )
    try:
        auth.update_user(uid, display_name=name)
    except Exception:
        logger.exception("Failed to update Auth display name for user %s.", uid)
    return name


def dismiss_preferred_name_prompt(uid: str) -> None:
    get_firestore_client().collection("users").document(uid).update(
        {
            "preferred_name_prompted": True,
            "updated_at": datetime.now(timezone.utc),
        }
    )


def get_user_profile(uid: str) -> dict:
    try:
        doc = get_firestore_client().collection("users").document(uid).get()
        return doc.to_dict() if doc.exists else {}
    except Exception:
        logger.exception("Failed to load Firestore profile for user %s.", uid)
        return {}


def build_chat_profile(user: auth.UserRecord) -> dict:
    profile = get_user_profile(user.uid)
    goal_race_date = _coerce_iso_date(profile.get("goal_race_date"))
    preferred_name = " ".join(str(profile.get("preferred_name") or "").split())
    display_name = (
        preferred_name
        or profile.get("display_name")
        or profile.get("full_name")
        or user.display_name
        or (user.email.split("@", 1)[0] if user.email else "Runner")
    )
    return {
        "uid": user.uid,
        "email": user.email or profile.get("email", ""),
        "display_name": display_name,
        "full_name": profile.get("full_name") or display_name,
        "preferred_name": preferred_name or None,
        "preferred_name_prompted": profile.get("preferred_name_prompted"),
        "age": profile.get("age"),
        "weight_kg": profile.get("weight_kg"),
        "sex": profile.get("sex"),
        "fitness_level": profile.get("fitness_level"),
        "goal_distance": profile.get("goal_distance"),
        "goal_race_date": goal_race_date,
        "current_weekly_km": profile.get("current_weekly_km"),
        "training_days_per_week": profile.get("training_days_per_week"),
        "training_days": profile.get("training_days") or [],
        "preferred_long_run_day": profile.get("preferred_long_run_day"),
        "recent_race_time": profile.get("recent_race_time"),
        "injury_flag": bool(profile.get("injury_flag", False)),
        "onboarding_completed": bool(profile.get("onboarding_completed", False)),
        "active_plan_id": profile.get("active_plan_id"),
    }
