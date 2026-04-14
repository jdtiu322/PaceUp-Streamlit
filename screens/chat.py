from __future__ import annotations

import html
import re

import streamlit as st

from services.firebase import build_chat_profile
from services.firestore_chat import create_chat_session, load_chat_sessions, load_messages_for_session, save_message_to_firestore
from services.gemini import get_gemini_response
from state import logout_user

CHAT_SESSIONS_HEIGHT = 420
CHAT_MESSAGES_HEIGHT = 520


def _start_new_chat() -> None:
    st.session_state.messages = []
    st.session_state.active_session_id = None
    st.rerun()


def _open_chat_session(user_uid: str, session_id: str) -> None:
    st.session_state.active_session_id = session_id
    st.session_state.messages = load_messages_for_session(user_uid, session_id)
    st.rerun()


def _submit_chat_turn(user_uid: str, profile: dict, prompt: str) -> None:
    if not st.session_state.active_session_id:
        sid = create_chat_session(user_uid, prompt)
        st.session_state.active_session_id = sid
        st.session_state.chat_sessions = load_chat_sessions(user_uid)

    sid = st.session_state.active_session_id
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message_to_firestore(user_uid, sid, "user", prompt)

    with st.spinner("PaceUp is thinking..."):
        reply = get_gemini_response(st.session_state.messages, profile)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    save_message_to_firestore(user_uid, sid, "assistant", reply)
    st.rerun()


def _format_message_content(content: str, *, role: str) -> str:
    text = (content or "").replace("\r\n", "\n").strip()
    if role == "assistant":
        text = re.sub(r"\n[ \t]*\n+", "\n", text)
        return text
    return html.escape(text)


def _render_chat_dock(prompts: list[str], *, empty_state: bool = False) -> tuple[str | None, str | None, bool]:
    triggered_prompt = None
    user_input = None
    send = False

    container_key = "chat_dock_empty" if empty_state else "chat_dock"
    inner_key = "chat_dock_empty_inner" if empty_state else "chat_dock_inner"
    suggestions_key = "chat_suggestions_empty" if empty_state else "chat_suggestions"
    input_key = "chat_input_empty" if empty_state else "chat_input"
    form_key = "chat_input_form_empty" if empty_state else "chat_input_form"
    send_wrap_key = "send_btn_empty" if empty_state else "send_btn"
    input_widget_key = "msg_input_empty" if empty_state else "msg_input"

    with st.container(key=container_key):
        with st.container(key=inner_key):
            if empty_state:
                with st.container(key=input_key):
                    with st.form(form_key, clear_on_submit=True):
                        ic, bc = st.columns([0.92, 0.08], gap="small")
                        with ic:
                            user_input = st.text_input(
                                "msg",
                                placeholder="Ask PaceUp about your next run, pacing, fueling, or recovery...",
                                label_visibility="collapsed",
                                key=input_widget_key,
                            )
                        with bc:
                            with st.container(key=send_wrap_key):
                                send = st.form_submit_button("Send", use_container_width=True)

                with st.container(key=suggestions_key):
                    qp_cols = st.columns(5)
                    for i, (col, prompt) in enumerate(zip(qp_cols, prompts)):
                        with col:
                            if st.button(prompt, key=f"qp_empty_{i}", use_container_width=True):
                                triggered_prompt = prompt
            else:
                with st.container(key=suggestions_key):
                    qp_cols = st.columns(5)
                    for i, (col, prompt) in enumerate(zip(qp_cols, prompts)):
                        with col:
                            if st.button(prompt, key=f"qp_{i}", use_container_width=True):
                                triggered_prompt = prompt

                with st.container(key=input_key):
                    with st.form(form_key, clear_on_submit=True):
                        ic, bc = st.columns([0.92, 0.08], gap="small")
                        with ic:
                            user_input = st.text_input(
                                "msg",
                                placeholder="Ask PaceUp about your next run, pacing, fueling, or recovery...",
                                label_visibility="collapsed",
                                key=input_widget_key,
                            )
                        with bc:
                            with st.container(key=send_wrap_key):
                                send = st.form_submit_button("Send", use_container_width=True)

            st.markdown(
                '<div class="disclaimer">PaceUp can make mistakes. For pain, injury, or medical concerns, check with a qualified professional.</div>',
                unsafe_allow_html=True,
            )

    return triggered_prompt, user_input, send


def show_chat() -> None:
    user = st.session_state.user
    profile = build_chat_profile(user)
    st.session_state.user_profile = profile

    name = profile.get("display_name") or user.email.split("@", 1)[0]
    initials = "".join(word[0].upper() for word in name.split()[:2]) or "P"
    goal = profile.get("goal_distance", "Marathon Training")

    if not st.session_state.chat_sessions:
        st.session_state.chat_sessions = load_chat_sessions(user.uid)

    prompts = ["Generate my plan", "Nutrition tips", "Recovery advice", "Pace calculator", "Race day tips"]
    triggered_prompt = None
    user_input = None
    send = False
    is_empty = not st.session_state.messages

    with st.container(key="chat_shell"):
        sidebar_col, main_col = st.columns([0.22, 0.78], gap="medium")

        with sidebar_col:
            with st.container(key="chat_sidebar"):
                with st.container(key="chat_sidebar_top"):
                    st.markdown(
                        """
                        <div class="chat-sidebar-header">
                            <div class="sidebar-logo"><span class="lp">PACE</span><span class="lu">UP</span></div>
                            <div class="sidebar-subtle">Coach workspace</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    with st.container(key="new_chat_btn"):
                        if st.button("+ New chat", key="btn_new_chat", use_container_width=True):
                            _start_new_chat()
                    st.markdown('<div class="sidebar-section-label">Recent chats</div>', unsafe_allow_html=True)
                    with st.container(key="chat_sessions", height=CHAT_SESSIONS_HEIGHT, border=False):
                        sessions = st.session_state.chat_sessions
                        if sessions:
                            for session in sessions:
                                title = session.get("title", "New conversation")
                                is_active = session["id"] == st.session_state.active_session_id
                                if st.button(
                                    title,
                                    key=f"sess_{session['id']}",
                                    type="primary" if is_active else "secondary",
                                    use_container_width=True,
                                ):
                                    _open_chat_session(user.uid, session["id"])
                        else:
                            st.markdown('<div class="chat-empty-history">No chats yet</div>', unsafe_allow_html=True)

                with st.container(key="chat_sidebar_footer"):
                    st.markdown(
                        f"""
                        <div class="user-card">
                            <div class="user-avatar">{initials}</div>
                            <div>
                                <div class="user-name">{html.escape(name)}</div>
                                <div class="user-email">{html.escape(user.email)}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    with st.container(key="signout_sidebar"):
                        if st.button("Sign out", key="btn_signout_chat", use_container_width=True):
                            logout_user()

        with main_col:
            with st.container(key="chat_main"):
                with st.container(key="chat_header"):
                    st.markdown(
                        f"""
                        <div class="chat-header-bar">
                            <div>
                                <div class="chat-header-title">PaceUp Coach</div>
                                <div class="chat-header-sub">Personalized support for {html.escape(str(goal))}</div>
                            </div>
                            <div class="chat-goal-pill">{html.escape(str(goal))}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with st.container(key="chat_body", height="content" if is_empty else CHAT_MESSAGES_HEIGHT, border=False):
                    with st.container(key="chat_body_inner"):
                        if is_empty:
                            st.markdown(
                                f"""
                                <div class="empty-chat">
                                    <div class="empty-chat-copy">
                                        <div class="empty-chat-kicker">PaceUp</div>
                                        <div class="empty-chat-title">Hey {html.escape(name)}, ready to train smarter?</div>
                                        <div class="empty-chat-sub">Ask for a weekly plan, a long-run strategy, nutrition guidance, pacing help, or recovery support.</div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            triggered_prompt, user_input, send = _render_chat_dock(prompts, empty_state=True)
                        else:
                            st.markdown('<div class="chat-msg-wrap">', unsafe_allow_html=True)
                            for msg in st.session_state.messages:
                                role = msg["role"]
                                content = msg["content"]
                                is_user = role == "user"
                                formatted_content = _format_message_content(content, role=role)
                                if is_user:
                                    st.markdown(
                                        f"""
                                        <div class="chat-msg user-msg">
                                            <div class="msg-inner">
                                                <div class="msg-bubble">{formatted_content}</div>
                                            </div>
                                        </div>
                                        """,
                                        unsafe_allow_html=True,
                                    )
                                else:
                                    st.markdown(
                                        """
                                        <div class="chat-msg">
                                            <div class="msg-inner">
                                                <div class="assistant-response">
                                        """,
                                        unsafe_allow_html=True,
                                    )
                                    st.markdown(formatted_content)
                                    st.markdown(
                                        """
                                                </div>
                                            </div>
                                        </div>
                                        """,
                                        unsafe_allow_html=True,
                                    )
                            st.markdown("</div>", unsafe_allow_html=True)

                if not is_empty:
                    triggered_prompt, user_input, send = _render_chat_dock(prompts)

            final_input = triggered_prompt or (user_input.strip() if (send and user_input and user_input.strip()) else None)

            if final_input:
                _submit_chat_turn(user.uid, profile, final_input)
