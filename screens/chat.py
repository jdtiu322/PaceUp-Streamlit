from __future__ import annotations

import html
from datetime import datetime, timedelta, timezone

import streamlit as st

from services.firebase import build_chat_profile
from services.firestore_chat import (
    create_chat_session,
    load_chat_sessions,
    load_older_messages_page,
    load_recent_messages_page,
    save_message_to_firestore,
)
from services.gemini import stream_gemini_response
from services.telemetry import log_event
from state import logout_user


MODEL_CONTEXT_MESSAGE_LIMIT = 20
SUGGESTED_PROMPTS: tuple[tuple[str, str], ...] = (
    ("Plan week", "Plan my next training week"),
    ("Long run", "Help me plan my next long run"),
    ("Pacing", "Calculate a smart pace for my next workout"),
    ("Recovery", "Give me recovery advice for today"),
)


def _fallback_user_name(user) -> str:
    email = getattr(user, "email", "") or ""
    return email.split("@", 1)[0] if email else "Runner"


def _profile_display_name(user, profile: dict) -> str:
    for key in ("full_name", "display_name"):
        value = str(profile.get(key) or "").strip()
        if value:
            return value
    value = str(getattr(user, "display_name", "") or "").strip()
    return value or _fallback_user_name(user)


def _profile_initials(name: str) -> str:
    parts = [part for part in name.replace("-", " ").split() if part]
    return "".join(part[0].upper() for part in parts[:2]) or "P"


def _set_visible_messages(messages: list[dict], cursor: str | None, has_more: bool) -> None:
    st.session_state.messages = messages
    st.session_state.messages_cursor = cursor
    st.session_state.chat_has_more_messages = has_more


def _trim_model_context(messages: list[dict], limit: int = MODEL_CONTEXT_MESSAGE_LIMIT) -> list[dict]:
    return list(messages[-limit:])


def _get_cached_chat_profile(user) -> dict:
    cached_uid = st.session_state.get("user_profile_uid")
    cached_profile = st.session_state.get("user_profile") or {}
    if cached_uid == user.uid and cached_profile:
        display_name = _profile_display_name(user, cached_profile)
        cached_profile["display_name"] = display_name
        cached_profile["full_name"] = cached_profile.get("full_name") or display_name
        return cached_profile

    profile = build_chat_profile(user)
    display_name = _profile_display_name(user, profile)
    profile["display_name"] = display_name
    profile["full_name"] = profile.get("full_name") or display_name
    st.session_state.user_profile = profile
    st.session_state.user_profile_uid = user.uid
    return profile


def _start_new_chat() -> None:
    _set_visible_messages([], None, False)
    st.session_state.active_session_id = None
    st.session_state.active_chat_id = None
    st.session_state.pending_assistant_session_id = None
    st.session_state.pending_assistant_messages = []


def _open_chat_session(user_uid: str, session_id: str) -> None:
    st.session_state.active_session_id = session_id
    st.session_state.active_chat_id = session_id
    st.session_state.pending_assistant_session_id = None
    st.session_state.pending_assistant_messages = []
    messages, cursor, has_more = load_recent_messages_page(user_uid, session_id)
    _set_visible_messages(messages, cursor, has_more)


def _ensure_active_session_messages(user_uid: str) -> None:
    active_id = st.session_state.get("active_session_id") or st.session_state.get("active_chat_id")
    if not active_id:
        return

    st.session_state.active_session_id = active_id
    st.session_state.active_chat_id = active_id
    if st.session_state.get("messages"):
        return

    messages, cursor, has_more = load_recent_messages_page(user_uid, active_id)
    _set_visible_messages(messages, cursor, has_more)


def _load_older_messages(user_uid: str, session_id: str) -> None:
    older_messages, cursor, has_more = load_older_messages_page(
        user_uid, session_id, st.session_state.get("messages_cursor")
    )
    if older_messages:
        st.session_state.messages = older_messages + list(st.session_state.messages)
    st.session_state.messages_cursor = cursor
    st.session_state.chat_has_more_messages = has_more


def _queue_chat_turn(user_uid: str, prompt: str) -> None:
    if not st.session_state.active_session_id:
        sid = create_chat_session(user_uid, prompt)
        st.session_state.active_session_id = sid
        st.session_state.active_chat_id = sid
        st.session_state.chat_sessions = load_chat_sessions(user_uid)

    sid = st.session_state.active_session_id
    conversation_messages = list(st.session_state.messages)

    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message_to_firestore(user_uid, sid, "user", prompt)
    st.session_state.pending_assistant_session_id = sid
    st.session_state.pending_assistant_messages = _trim_model_context(
        conversation_messages + [{"role": "user", "content": prompt}]
    )


def _submit_chat_turn(user_uid: str, prompt: str, source: str, prompt_label: str | None = None) -> None:
    final_prompt = (prompt or "").strip()
    if not final_prompt:
        return

    log_event(
        user_uid,
        "chat_prompt_submitted",
        {
            "session_id": st.session_state.active_session_id,
            "source": source,
            "prompt_label": prompt_label,
        },
    )
    _queue_chat_turn(user_uid, final_prompt)


def _render_streaming_assistant_response(user_uid: str, profile: dict) -> bool:
    sid = st.session_state.get("pending_assistant_session_id")
    if not sid or sid != st.session_state.get("active_session_id"):
        return False

    messages = st.session_state.get("pending_assistant_messages") or list(st.session_state.messages)
    reply = st.write_stream(stream_gemini_response(messages, profile))
    if isinstance(reply, list):
        reply = "".join(str(part) for part in reply)
    reply = str(reply or "").strip()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    save_message_to_firestore(user_uid, sid, "assistant", reply)
    log_event(user_uid, "gemini_response_completed", {"session_id": sid, "reply_length": len(reply)})
    st.session_state.pending_assistant_session_id = None
    st.session_state.pending_assistant_messages = []
    return True


def _format_message_content(content: str, *, role: str) -> str:
    text = (content or "").replace("\r\n", "\n").strip()
    if role == "user":
        return html.escape(text)
    return text


def _coerce_timestamp(value) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except Exception:
            return None
    return None


def _session_id(session: dict) -> str:
    return str(session.get("id") or "").strip()


def _session_title(session: dict) -> str:
    return str(session.get("conversation_title") or session.get("title") or "New conversation").strip() or "New conversation"


def _unique_sessions_by_id(sessions: list[dict]) -> list[dict]:
    seen_ids: set[str] = set()
    unique_sessions: list[dict] = []
    for session in sessions:
        session_id = _session_id(session)
        if session_id:
            if session_id in seen_ids:
                continue
            seen_ids.add(session_id)
        unique_sessions.append(session)
    return unique_sessions


def _group_sessions_by_period(sessions: list[dict]) -> list[tuple[str, list[dict]]]:
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    week_start = today_start - timedelta(days=7)

    groups: dict[str, list[dict]] = {"Today": [], "Yesterday": [], "This week": [], "Earlier": []}
    for session in _unique_sessions_by_id(sessions):
        ts = _coerce_timestamp(session.get("updated_at") or session.get("created_at"))
        if ts is None:
            label = "Earlier"
        elif ts >= today_start:
            label = "Today"
        elif ts >= yesterday_start:
            label = "Yesterday"
        elif ts >= week_start:
            label = "This week"
        else:
            label = "Earlier"

        groups[label].append(session)
    return [(label, items) for label, items in groups.items() if items]


def _messages_for_display(messages: list[dict], active_session_title: str) -> list[dict]:
    display_messages = [dict(message) for message in messages]
    title = (active_session_title or "").strip()

    if title.casefold() != "generate my plan" or not display_messages:
        return display_messages

    first_assistant_index = next(
        (i for i, message in enumerate(display_messages) if message.get("role") == "assistant"),
        None,
    )
    canonical_user_message = {"role": "user", "content": title}

    if first_assistant_index is None:
        if display_messages[0].get("role") == "user":
            display_messages[0]["content"] = title
        else:
            display_messages.insert(0, canonical_user_message)
        return display_messages

    return [canonical_user_message] + display_messages[first_assistant_index:]


def _filter_sessions(sessions: list[dict], query: str) -> list[dict]:
    q = (query or "").strip().lower()
    if not q:
        return sessions
    return [s for s in sessions if q in _session_title(s).lower()]


def _render_suggestion_chips(user_uid: str) -> None:
    with st.container(key="chat_suggestions_empty"):
        columns = st.columns(len(SUGGESTED_PROMPTS), gap="small")
        for index, ((label, prompt), column) in enumerate(zip(SUGGESTED_PROMPTS, columns)):
            with column:
                st.button(
                    label,
                    key=f"chat_suggestion_{index}",
                    use_container_width=True,
                    on_click=_submit_chat_turn,
                    args=(user_uid, prompt, "suggestion", label),
                )


def show_chat() -> None:
    user = st.session_state.user
    profile = _get_cached_chat_profile(user)

    name = _profile_display_name(user, profile)
    initials = _profile_initials(name)
    goal = profile.get("goal_distance", "Marathon Training")
    plan_label = profile.get("goal_distance") or "Training plan"

    if not st.session_state.chat_sessions:
        st.session_state.chat_sessions = load_chat_sessions(user.uid)

    _ensure_active_session_messages(user.uid)

    is_empty = not st.session_state.messages
    st.markdown('<div class="chat-page-bg"></div>', unsafe_allow_html=True)

    active_session_title = ""
    if st.session_state.active_session_id:
        for session in st.session_state.chat_sessions:
            if session.get("id") == st.session_state.active_session_id:
                active_session_title = _session_title(session)
                break

    with st.container(key="chat_shell"):
        sidebar_col, main_col = st.columns([0.22, 0.78], gap="small")

        with sidebar_col:
            with st.container(key="chat_sidebar"):
                with st.container(key="chat_sidebar_top"):
                    st.markdown(
                        """
                        <div class="chat-brand-row">
                            <div class="chat-brand">
                                <span class="chat-brand-mark">P</span>
                                <span class="chat-brand-name">PaceUp</span>
                            </div>
                            <span class="chat-brand-plus">+</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    with st.container(key="new_chat_btn"):
                        st.button(
                            "+ New conversation",
                            key="btn_new_chat",
                            use_container_width=True,
                            on_click=_start_new_chat,
                        )

                    with st.container(key="chat_search"):
                        search_query = st.text_input(
                            "Search conversations",
                            placeholder="Search conversations",
                            key="chat_search_query",
                            label_visibility="collapsed",
                        )

                with st.container(key="chat_sessions", height=300, border=False):
                    sessions = _filter_sessions(st.session_state.chat_sessions, search_query)
                    if not sessions:
                        st.markdown(
                            '<div class="chat-empty-history">No conversations yet</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        groups = _group_sessions_by_period(sessions)
                        for label, items in groups:
                            st.markdown(
                                f'<div class="sidebar-section-label">{html.escape(label)}</div>',
                                unsafe_allow_html=True,
                            )
                            for session in items:
                                session_id = _session_id(session)
                                if not session_id:
                                    continue
                                title = _session_title(session)
                                is_active = session_id == st.session_state.active_session_id
                                st.button(
                                    title,
                                    key=f"sess_{session_id}",
                                    type="primary" if is_active else "secondary",
                                    use_container_width=True,
                                    on_click=_open_chat_session,
                                    args=(user.uid, session_id),
                                )

                with st.container(key="chat_sidebar_footer"):
                    st.markdown(
                        f"""
                        <div class="user-card">
                            <div class="user-avatar">{html.escape(initials)}</div>
                            <div class="user-card-text">
                                <div class="user-name">{html.escape(name)}</div>
                                <div class="user-email">{html.escape(plan_label)}</div>
                            </div>
                            <div class="user-card-chevron">v</div>
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
                    header_sub = active_session_title or f"Personalized support for {goal}"
                    st.markdown(
                        f"""
                        <div class="chat-header-bar">
                            <div class="chat-header-left">
                                <div class="chat-header-avatar">P</div>
                                <div class="chat-header-titles">
                                    <div class="chat-header-title">PaceUp Coach</div>
                                    <div class="chat-header-sub">{html.escape(header_sub)}</div>
                                </div>
                            </div>
                            <div class="chat-header-right">
                                <span class="chat-online-pill"><span class="pill-dot"></span>Online</span>
                                <span class="chat-header-icon" title="Share">share</span>
                                <span class="chat-header-icon" title="More">...</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with st.container(key="chat_body", height="stretch", border=False):
                    with st.container(key="chat_body_inner"):
                        if is_empty:
                            st.markdown(
                                f"""
                                <div class="empty-chat">
                                    <div class="empty-chat-copy">
                                        <div class="empty-chat-kicker"><span></span> PaceUp Coach</div>
                                        <div class="empty-chat-title">Hey {html.escape(name)}, ready to train smarter?</div>
                                        <div class="empty-chat-sub">Ask for a weekly plan, a long-run strategy, nutrition guidance, pacing help, or recovery support.</div>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            _render_suggestion_chips(user.uid)
                        else:
                            streamed_reply_finished = False
                            if st.session_state.get("chat_has_more_messages"):
                                st.button(
                                    "Load older messages",
                                    key="btn_load_older_messages",
                                    use_container_width=False,
                                    on_click=_load_older_messages,
                                    args=(user.uid, st.session_state.active_session_id),
                                )

                            for msg in _messages_for_display(st.session_state.messages, active_session_title):
                                role = msg["role"]
                                content = msg["content"]
                                is_user = role == "user"
                                formatted_content = _format_message_content(content, role=role)
                                if is_user:
                                    st.markdown(
                                        f"""<div class="chat-msg user-msg"><div class="msg-inner"><div class="msg-bubble">{formatted_content}</div></div><div class="msg-avatar user-avatar-sm">{html.escape(initials)}</div></div>""",
                                        unsafe_allow_html=True,
                                    )
                                else:
                                    st.markdown(
                                        f"""<div class="chat-msg assistant-msg">
<div class="msg-avatar coach-avatar-sm">P</div>
<div class="msg-inner">
<div class="assistant-response">

{formatted_content}

</div>
</div>
</div>""",
                                        unsafe_allow_html=True,
                                    )

                            if st.session_state.get("pending_assistant_session_id") == st.session_state.active_session_id:
                                with st.container(key="streaming_msg"):
                                    avatar_col, bubble_col = st.columns([0.07, 0.93], gap="small")
                                    with avatar_col:
                                        st.markdown(
                                            '<div class="msg-avatar coach-avatar-sm">P</div>',
                                            unsafe_allow_html=True,
                                        )
                                    with bubble_col:
                                        with st.container(key="streaming_bubble"):
                                            streamed_reply_finished = _render_streaming_assistant_response(user.uid, profile)
                            if streamed_reply_finished:
                                st.session_state.chat_sessions = load_chat_sessions(user.uid)
    prompt = st.chat_input(
        "Ask PaceUp anything - paces, training, recovery, race-day...",
        key="chat_input_prompt",
    )
    if prompt:
        _submit_chat_turn(user.uid, prompt, "typed")
        st.rerun()
