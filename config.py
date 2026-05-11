from __future__ import annotations

import base64
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def get_secret(name: str, default: str = "") -> str:
    try:
        if name in st.secrets:
            value = st.secrets[name]
            return str(value) if value is not None else default
    except Exception:
        pass
    return os.getenv(name, default)


FIREBASE_WEB_API_KEY = get_secret("FIREBASE_WEB_API_KEY", "")
GEMINI_API_KEY = get_secret("GEMINI_API_KEY", "")
GEMINI_MODEL = get_secret("GEMINI_MODEL", "gemini-2.5-flash-lite")
GEMINI_EMBEDDING_MODEL = get_secret("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")

_AUTH_COOKIE_SECURE_VALUE = get_secret("AUTH_COOKIE_SECURE", "").strip().lower()
# Local Streamlit usually runs over http://localhost, where Secure cookies are
# not persisted. Deployed HTTPS apps can opt in with AUTH_COOKIE_SECURE=true.
AUTH_COOKIE_SECURE = _AUTH_COOKIE_SECURE_VALUE in {"1", "true", "yes", "on"}


@st.cache_data(show_spinner=False)
def encode_image(name: str) -> str:
    path = BASE_DIR / name
    return base64.b64encode(path.read_bytes()).decode("utf-8") if path.exists() else ""


RUNNER_IMAGE = encode_image("runner.jpg")
LOGO_IMAGE = encode_image("paceup.png")

ONBOARDING_DAY_OPTIONS = [
    ("Monday", "M"),
    ("Tuesday", "Tu"),
    ("Wednesday", "W"),
    ("Thursday", "Th"),
    ("Friday", "F"),
    ("Saturday", "Sa"),
    ("Sunday", "Su"),
]

ONBOARDING_SEX_OPTIONS = ["Male", "Female", "Other", "Prefer not to say"]
ONBOARDING_GOAL_OPTIONS = ["5K", "10K", "Half Marathon", "Full Marathon", "Ultra Marathon"]

GOAL_DISTANCE_ALIASES = {
    "Half Marathon (21K)": "Half Marathon",
    "Full Marathon (42K)": "Full Marathon",
}

FITNESS_MAP = {
    "NOVICE": "Beginner - I rarely run",
    "INTER": "Intermediate - I run occasionally",
    "ELITE": "Advanced - I run regularly",
}

FITNESS_ALIASES = {
    "NOVICE": "NOVICE",
    "Novice": "NOVICE",
    "Beginner - I rarely run": "NOVICE",
    "INTER": "INTER",
    "Inter": "INTER",
    "Intermediate - I run occasionally": "INTER",
    "ELITE": "ELITE",
    "Elite": "ELITE",
    "Advanced - I run regularly": "ELITE",
}


def normalize_fitness_level(value: str | None) -> str:
    return FITNESS_ALIASES.get(value or "", "NOVICE")


def normalize_goal_distance(value: str | None) -> str:
    normalized = GOAL_DISTANCE_ALIASES.get(value or "", value or "Full Marathon")
    return normalized if normalized in ONBOARDING_GOAL_OPTIONS else "Full Marathon"
