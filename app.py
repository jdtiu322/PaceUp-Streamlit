from __future__ import annotations

import json

import streamlit as st
import streamlit.components.v1 as components

from components.navbar import render_nav
from components.styles import inject_styles
import config
from screens.chat import show_chat
from screens.landing import show_landing
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


def _auth_cookie_secure() -> bool:
    configured = getattr(config, "AUTH_COOKIE_SECURE", None)
    if configured is not None:
        return str(configured).strip().lower() in {"1", "true", "yes", "on"}
    get_secret = getattr(config, "get_secret", None)
    raw_value = get_secret("AUTH_COOKIE_SECURE", "") if callable(get_secret) else ""
    return str(raw_value).strip().lower() in {"1", "true", "yes", "on"}


AUTH_COOKIE_SECURE = _auth_cookie_secure()

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
        auth_token_script = f"""
            try {{
                var token = {json.dumps(pending_auth_token)};
                document.cookie = {json.dumps(f"{AUTH_COOKIE_NAME}=")} + encodeURIComponent(token) + {json.dumps(f"; Max-Age={AUTH_COOKIE_MAX_AGE}; Path=/; SameSite=Lax{secure_cookie}")};
            }} catch (e) {{}}
            try {{
                var token = {json.dumps(pending_auth_token)};
                window.localStorage.setItem({json.dumps(AUTH_COOKIE_NAME)}, token);
            }} catch (e) {{}}
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
            st.markdown("Restoring your session...")
            st.stop()

        attempts = int(st.session_state.get("auth_restore_attempts", 0))
        if attempts < MAX_AUTH_RESTORE_ATTEMPTS:
            st.session_state.auth_restore_attempted = True
            st.session_state.auth_restore_attempts = attempts + 1
            sync_page_to_url()
            secure_cookie = "; Secure" if AUTH_COOKIE_SECURE else ""
            components.html(
                f"""
                <script>
                    try {{
                        var restoreKey = {json.dumps(AUTH_COOKIE_NAME + "_restore_attempted")};
                        var token = window.localStorage.getItem({json.dumps(AUTH_COOKIE_NAME)});
                        var alreadyTried = window.sessionStorage.getItem(restoreKey) === "1";
                        if (token && !alreadyTried) {{
                            window.sessionStorage.setItem(restoreKey, "1");
                            try {{
                                document.cookie = {json.dumps(f"{AUTH_COOKIE_NAME}=")} + encodeURIComponent(token) + {json.dumps(f"; Max-Age={AUTH_COOKIE_MAX_AGE}; Path=/; SameSite=Lax{secure_cookie}")};
                            }} catch (e) {{}}
                            var bridgeKey = {json.dumps(AUTH_SESSION_QUERY_PARAM)};
                            function withBridge(href) {{
                                try {{
                                    var u = new URL(href, window.location.origin);
                                    u.searchParams.set(bridgeKey, token);
                                    return u.toString();
                                }} catch (e) {{
                                    var sep = href.indexOf("?") >= 0 ? "&" : "?";
                                    return href + sep + bridgeKey + "=" + encodeURIComponent(token);
                                }}
                            }}
                            setTimeout(function () {{
                                try {{
                                    var dest = withBridge(window.top.location.href);
                                    window.top.location.href = dest;
                                    return;
                                }} catch (e) {{}}
                                try {{
                                    var dest2 = withBridge(window.parent.location.href);
                                    window.parent.location.href = dest2;
                                    return;
                                }} catch (e) {{}}
                                try {{
                                    var dest3 = withBridge(window.location.href);
                                    window.location.href = dest3;
                                }} catch (e) {{}}
                            }}, 200);
                        }} else {{
                            setTimeout(function () {{
                                try {{
                                    window.top.location.href = "?page=login";
                                    return;
                                }} catch (e) {{}}
                                try {{
                                    window.parent.location.href = "?page=login";
                                    return;
                                }} catch (e) {{}}
                                try {{
                                    window.location.href = "?page=login";
                                }} catch (e) {{}}
                            }}, 120);
                        }}
                    }} catch (e) {{}}
                </script>
                """,
                height=0,
            )
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
elif st.session_state.user:
    onboarding_done = check_onboarding_status(st.session_state.user.uid)
    if st.session_state.page == "onboarding" or not onboarding_done:
        st.session_state.page = "onboarding"
        st.session_state.onboarding_completed = False
        sync_page_to_url()
        show_onboarding()
    else:
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
