from __future__ import annotations

import json

import streamlit as st
import streamlit.components.v1 as components

from components.navbar import render_nav
from components.styles import inject_styles
import config
from screens.chat import show_chat
from screens.landing import show_landing
from screens.legal import show_privacy, show_terms
from screens.login import show_login
from screens.onboarding import show_onboarding
from screens.placeholder import show_placeholder_page
from screens.register import show_register
from services import firebase as firebase_service
from state import go_to, init_state, restore_saved_session, set_flash, sync_page_to_url

PROTECTED_PAGES = {"onboarding", "chat"}
MAX_AUTH_RESTORE_ATTEMPTS = 3
AUTH_COOKIE_MAX_AGE = getattr(firebase_service, "AUTH_COOKIE_MAX_AGE", 60 * 60 * 24 * 30)
AUTH_COOKIE_NAME = getattr(firebase_service, "AUTH_COOKIE_NAME", "paceup_refresh_token")
AUTH_SESSION_QUERY_PARAM = getattr(firebase_service, "AUTH_SESSION_QUERY_PARAM", "_auth")
check_onboarding_status = firebase_service.check_onboarding_status
init_firebase = firebase_service.init_firebase
persist_auth_session = firebase_service.persist_auth_session


def _auth_cookie_secure() -> bool:
    configured = getattr(config, "AUTH_COOKIE_SECURE", None)
    if configured is not None:
        return str(configured).strip().lower() in {"1", "true", "yes", "on"}
    get_secret = getattr(config, "get_secret", None)
    raw_value = get_secret("AUTH_COOKIE_SECURE", "") if callable(get_secret) else ""
    return str(raw_value).strip().lower() in {"1", "true", "yes", "on"}


AUTH_COOKIE_SECURE = _auth_cookie_secure()


def _render_auth_restore_bridge(*, login_delay_ms: int = 900) -> None:
    secure_cookie = "; Secure" if AUTH_COOKIE_SECURE else ""
    components.html(
        f"""
        <script>
            try {{
                var authName = {json.dumps(AUTH_COOKIE_NAME)};
                var bridgeKey = {json.dumps(AUTH_SESSION_QUERY_PARAM)};
                var cookieAttrs = {json.dumps(f"; Max-Age={AUTH_COOKIE_MAX_AGE}; Path=/; SameSite=Lax{secure_cookie}")};
                var loginHref = "?page=login";

                function readStoredToken(targetWindow) {{
                    try {{ return targetWindow.localStorage.getItem(authName) || ""; }} catch (e) {{}}
                    return "";
                }}

                function readCookieToken(targetWindow) {{
                    try {{
                        var prefix = authName + "=";
                        var parts = (targetWindow.document.cookie || "").split(";");
                        for (var i = 0; i < parts.length; i += 1) {{
                            var part = parts[i].trim();
                            if (part.indexOf(prefix) === 0) {{
                                return decodeURIComponent(part.slice(prefix.length));
                            }}
                        }}
                    }} catch (e) {{}}
                    return "";
                }}

                function persistToken(targetWindow, token) {{
                    if (!targetWindow || !token) {{
                        return;
                    }}
                    try {{ targetWindow.localStorage.setItem(authName, token); }} catch (e) {{}}
                    try {{ targetWindow.sessionStorage.removeItem(authName + "_restore_attempted"); }} catch (e) {{}}
                    try {{ targetWindow.document.cookie = authName + "=" + encodeURIComponent(token) + cookieAttrs; }} catch (e) {{}}
                }}

                function withBridge(href, token) {{
                    try {{
                        var u = new URL(href, window.location.origin);
                        u.searchParams.set(bridgeKey, token);
                        return u.toString();
                    }} catch (e) {{
                        var sep = href.indexOf("?") >= 0 ? "&" : "?";
                        return href + sep + bridgeKey + "=" + encodeURIComponent(token);
                    }}
                }}

                function navigate(href) {{
                    try {{
                        window.top.location.href = href;
                        return true;
                    }} catch (e) {{}}
                    try {{
                        window.parent.location.href = href;
                        return true;
                    }} catch (e) {{}}
                    try {{ window.location.href = href; }} catch (e) {{}}
                    return false;
                }}

                var token = "";
                token = token || readStoredToken(window) || readCookieToken(window);
                try {{ token = token || readStoredToken(window.parent) || readCookieToken(window.parent); }} catch (e) {{}}
                try {{ token = token || readStoredToken(window.top) || readCookieToken(window.top); }} catch (e) {{}}

                if (token) {{
                    persistToken(window, token);
                    try {{ persistToken(window.parent, token); }} catch (e) {{}}
                    try {{ persistToken(window.top, token); }} catch (e) {{}}
                    setTimeout(function () {{
                        var href = window.location.href;
                        try {{ href = window.parent.location.href || href; }} catch (e) {{}}
                        try {{ href = window.top.location.href || href; }} catch (e) {{}}
                        navigate(withBridge(href, token));
                    }}, 200);
                }} else {{
                    setTimeout(function () {{
                        navigate(loginHref);
                    }}, {int(login_delay_ms)});
                }}
            }} catch (e) {{}}
        </script>
        """,
        height=0,
    )


st.set_page_config(
    page_title="PaceUp",
    page_icon=":runner:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_firebase()
init_state()
restore_saved_session()

if st.session_state.user is not None:
    # Reset the per-tab recovery guard so a future refresh can try again if the cookie drops.
    pending_auth_token = st.session_state.pop("pending_auth_token", "")
    secure_cookie = "; Secure" if AUTH_COOKIE_SECURE else ""
    auth_token_script = ""
    if pending_auth_token:
        persist_auth_session(pending_auth_token)
        auth_token_script = f"""
            var token = {json.dumps(pending_auth_token)};
            var authName = {json.dumps(AUTH_COOKIE_NAME)};
            var restoreKey = {json.dumps(AUTH_COOKIE_NAME + "_restore_attempted")};
            var cookieAttrs = {json.dumps(f"; Max-Age={AUTH_COOKIE_MAX_AGE}; Path=/; SameSite=Lax{secure_cookie}")};
            function persistToken(targetWindow) {{
                if (!targetWindow || !token) {{
                    return;
                }}
                try {{ targetWindow.localStorage.setItem(authName, token); }} catch (e) {{}}
                try {{ targetWindow.sessionStorage.removeItem(restoreKey); }} catch (e) {{}}
                try {{ targetWindow.document.cookie = authName + "=" + encodeURIComponent(token) + cookieAttrs; }} catch (e) {{}}
            }}
            persistToken(window);
            try {{ persistToken(window.parent); }} catch (e) {{}}
            try {{ persistToken(window.top); }} catch (e) {{}}
        """
    components.html(
        f"""
        <script>
            {auth_token_script}
            try {{ window.sessionStorage.removeItem({json.dumps(AUTH_COOKIE_NAME + "_restore_attempted")}); }} catch (e) {{}}
        </script>
        """,
        height=0,
    )

if st.session_state.page in PROTECTED_PAGES and not st.session_state.user:
    if not st.session_state.get("signed_out"):
        if not st.session_state.get("auth_bridge_ready", True):
            _render_auth_restore_bridge(login_delay_ms=1200)
            st.markdown("Restoring your session...")
            st.stop()

        attempts = int(st.session_state.get("auth_restore_attempts", 0))
        if attempts < MAX_AUTH_RESTORE_ATTEMPTS:
            st.session_state.auth_restore_attempted = True
            st.session_state.auth_restore_attempts = attempts + 1
            sync_page_to_url()
            _render_auth_restore_bridge()
            st.markdown("Restoring your session...")
            st.stop()
        else:
            st.session_state.auth_restore_attempted = False
            st.session_state.auth_restore_attempts = 0
            set_flash("error", "Please sign in to continue.")
            go_to("login")
    else:
        st.session_state.auth_restore_attempted = False
        st.session_state.auth_restore_attempts = 0
        set_flash("error", "Please sign in to continue.")
        go_to("login")

sync_page_to_url()
inject_styles()

if st.session_state.get("theme") == "dark":
    st.markdown('<div class="theme-dark-marker" hidden></div>', unsafe_allow_html=True)

if st.session_state.page in {"about", "contact"}:
    render_nav()

if st.session_state.page == "home":
    show_landing()
elif st.session_state.page == "about":
    show_placeholder_page("About", "This is about page")
elif st.session_state.page == "contact":
    show_placeholder_page("Contact", "This is contact page")
elif st.session_state.page == "terms":
    show_terms()
elif st.session_state.page == "privacy":
    show_privacy()
elif st.session_state.user:
    onboarding_done = check_onboarding_status(st.session_state.user.uid)
    if st.session_state.page == "onboarding" or not onboarding_done:
        st.session_state.page = "onboarding"
        st.session_state.onboarding_completed = False
        sync_page_to_url()
        show_onboarding()
    else:
        if st.session_state.page != "chat":
            st.session_state.page = "chat"
        st.session_state.onboarding_completed = True
        sync_page_to_url()
        show_chat()
elif st.session_state.page == "register":
    show_register()
elif st.session_state.page == "login":
    show_login()
else:
    show_login()
