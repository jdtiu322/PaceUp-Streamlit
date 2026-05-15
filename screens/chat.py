from __future__ import annotations

import html
import re
from datetime import date, datetime, timedelta, timezone

import streamlit as st

from services.firestore_plan import (
    apply_plan_patch,
    build_plan_context,
    get_plan_dashboard,
    save_run_progress_entry,
    update_workout_status,
)
from services.firebase import build_chat_profile, dismiss_preferred_name_prompt, save_preferred_name, update_goal_race_date
from services.firestore_chat import (
    create_chat_session,
    delete_chat_session,
    load_chat_sessions,
    load_older_messages_page,
    load_recent_messages_page,
    rename_chat_session,
    save_message_to_firestore,
)
from services.gemini import generate_plan_patch, stream_gemini_response
from services.rag import collect_source_citations, retrieve_context
from services.run_screenshot import analyze_run_screenshot
from services.telemetry import log_event
from state import logout_user


MODEL_CONTEXT_MESSAGE_LIMIT = 20
SUGGESTED_PROMPTS: tuple[tuple[str, str], ...] = (
    ("Plan week", "Plan my next training week"),
    ("Long run", "Help me plan my next long run"),
    ("Pacing", "Calculate a smart pace for my next workout"),
    ("Recovery", "Give me recovery advice for today"),
)

RACE_DATE_UPDATE_KEYWORDS = (
    "target race date",
    "target date",
    "race date",
    "race day",
    "goal race date",
    "goal date",
)

MONTH_ALIASES = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def _fallback_user_name(user) -> str:
    email = getattr(user, "email", "") or ""
    return email.split("@", 1)[0] if email else "Runner"


def _profile_display_name(user, profile: dict) -> str:
    for key in ("preferred_name", "display_name", "full_name"):
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


def _latest_user_message(messages: list[dict]) -> str:
    return next(
        (str(message.get("content") or "") for message in reversed(messages) if message.get("role") == "user"),
        "",
    )


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


def _should_show_name_prompt(profile: dict) -> bool:
    if st.session_state.get("show_name_prompt_after_onboarding"):
        return True
    return profile.get("preferred_name_prompted") is False


def _close_name_prompt() -> None:
    st.session_state.show_name_prompt_after_onboarding = False
    st.session_state.preferred_name_input = ""
    st.session_state.preferred_name_dialog_initialized = False
    st.session_state.pop("preferred_name_dialog_error", None)


@st.dialog("What should I call you?")
def _preferred_name_dialog(user_uid: str, current_name: str) -> None:
    st.markdown(
        '<p class="name-dialog-copy">Choose the name PaceUp should use in coaching conversations.</p>',
        unsafe_allow_html=True,
    )
    if not st.session_state.get("preferred_name_dialog_initialized"):
        st.session_state.preferred_name_input = current_name
        st.session_state.preferred_name_dialog_initialized = True
    name = st.text_input(
        "Preferred name",
        placeholder="e.g. Maya",
        key="preferred_name_input",
    )

    error = st.session_state.get("preferred_name_dialog_error")
    if error:
        st.markdown(f'<div class="flash flash-error">{html.escape(error)}</div>', unsafe_allow_html=True)

    save_col, skip_col = st.columns(2)
    with save_col:
        if st.button("Save name", key="save_preferred_name", type="primary", use_container_width=True):
            cleaned = " ".join((name or "").split())
            if not cleaned:
                st.session_state.preferred_name_dialog_error = "Enter a name, or skip for now."
                st.rerun()
            try:
                saved = save_preferred_name(user_uid, cleaned)
                if saved:
                    profile = dict(st.session_state.get("user_profile") or {})
                    profile["display_name"] = saved
                    profile["full_name"] = profile.get("full_name") or saved
                    profile["preferred_name"] = saved
                    profile["preferred_name_prompted"] = True
                    st.session_state.user_profile = profile
                log_event(user_uid, "preferred_name_saved", {"source": "post_onboarding_prompt"})
                _close_name_prompt()
                st.rerun()
            except Exception as exc:
                st.session_state.preferred_name_dialog_error = f"Could not save name: {exc}"
                st.rerun()
    with skip_col:
        if st.button("Skip for now", key="skip_preferred_name", use_container_width=True):
            try:
                dismiss_preferred_name_prompt(user_uid)
                profile = dict(st.session_state.get("user_profile") or {})
                profile["preferred_name_prompted"] = True
                st.session_state.user_profile = profile
                log_event(user_uid, "preferred_name_prompt_skipped", {"source": "post_onboarding_prompt"})
                _close_name_prompt()
                st.rerun()
            except Exception as exc:
                st.session_state.preferred_name_dialog_error = f"Could not dismiss prompt: {exc}"
                st.rerun()


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


def _rename_chat_session(user_uid: str, session_id: str) -> None:
    raw = st.session_state.get(f"rename_input_{session_id}", "")
    title = (raw or "").strip()
    if not title:
        return
    saved = rename_chat_session(user_uid, session_id, title)
    if not saved:
        return
    for session in st.session_state.chat_sessions:
        if session.get("id") == session_id:
            session["title"] = saved
            session["conversation_title"] = saved
            break


def _delete_chat_session(user_uid: str, session_id: str) -> None:
    if not delete_chat_session(user_uid, session_id):
        return
    st.session_state.chat_sessions = [
        s for s in st.session_state.chat_sessions if s.get("id") != session_id
    ]
    if st.session_state.get("active_session_id") == session_id:
        _start_new_chat()


@st.dialog("Edit conversation")
def _edit_conversation_dialog(user_uid: str, session_id: str, current_title: str) -> None:
    new_title = st.text_input(
        "Conversation title",
        value=current_title,
        key=f"dlg_rename_{session_id}",
    )
    save_col, delete_col = st.columns(2)
    with save_col:
        if st.button("Save", key=f"dlg_save_{session_id}", use_container_width=True, type="primary"):
            saved = rename_chat_session(user_uid, session_id, new_title)
            if saved:
                for s in st.session_state.chat_sessions:
                    if s.get("id") == session_id:
                        s["title"] = saved
                        s["conversation_title"] = saved
                        break
            st.session_state.pop("editing_session_id", None)
            st.session_state.pop("editing_session_title", None)
            st.rerun()
    with delete_col:
        if st.button("Delete", key=f"dlg_delete_{session_id}", use_container_width=True):
            if delete_chat_session(user_uid, session_id):
                st.session_state.chat_sessions = [
                    s for s in st.session_state.chat_sessions if s.get("id") != session_id
                ]
                if st.session_state.get("active_session_id") == session_id:
                    _start_new_chat()
            st.session_state.pop("editing_session_id", None)
            st.session_state.pop("editing_session_title", None)
            st.rerun()


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


def _format_short_date(value: date) -> str:
    return f"{value:%b} {value.day}, {value.year}"


def _date_from_parts(year: int, month: int, day: int) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _extract_target_race_date(text: str) -> date | None:
    lower = (text or "").casefold()
    if not any(keyword in lower for keyword in RACE_DATE_UPDATE_KEYWORDS):
        return None

    iso_match = re.search(r"\b(20\d{2})-(\d{1,2})-(\d{1,2})\b", text)
    if iso_match:
        parsed = _date_from_parts(int(iso_match.group(1)), int(iso_match.group(2)), int(iso_match.group(3)))
        if parsed:
            return parsed

    numeric_match = re.search(r"\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b", text)
    if numeric_match:
        parsed = _date_from_parts(
            int(numeric_match.group(3)),
            int(numeric_match.group(1)),
            int(numeric_match.group(2)),
        )
        if parsed:
            return parsed

    month_names = "|".join(sorted(MONTH_ALIASES, key=len, reverse=True))
    month_match = re.search(
        rf"\b({month_names})\.?\s+(\d{{1,2}})(?:st|nd|rd|th)?[,]?\s+(20\d{{2}})\b",
        text,
        re.IGNORECASE,
    )
    if month_match:
        parsed = _date_from_parts(
            int(month_match.group(3)),
            MONTH_ALIASES[month_match.group(1).casefold()],
            int(month_match.group(2)),
        )
        if parsed:
            return parsed

    day_month_match = re.search(
        rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+({month_names})\.?[,]?\s+(20\d{{2}})\b",
        text,
        re.IGNORECASE,
    )
    if day_month_match:
        parsed = _date_from_parts(
            int(day_month_match.group(3)),
            MONTH_ALIASES[day_month_match.group(2).casefold()],
            int(day_month_match.group(1)),
        )
        if parsed:
            return parsed

    return None


def _maybe_apply_target_race_date_update(user_uid: str, prompt: str) -> None:
    target_date = _extract_target_race_date(prompt)
    if not target_date:
        return
    if target_date < date.today():
        st.session_state.plan_update_error = "Target race date must be today or later."
        return

    normalized_date = update_goal_race_date(user_uid, target_date)
    cached_profile = dict(st.session_state.get("user_profile") or {})
    cached_profile["goal_race_date"] = normalized_date
    st.session_state.user_profile = cached_profile
    st.session_state.plan_dashboard_dirty = True
    st.session_state.plan_update_notice = {
        "summary": f"Target race date updated to {_format_short_date(target_date)}.",
    }
    log_event(user_uid, "target_race_date_updated", {"goal_race_date": normalized_date})


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
    try:
        _maybe_apply_target_race_date_update(user_uid, final_prompt)
    except Exception:
        st.session_state.plan_update_error = "I could not update the target race date from that message."
    _queue_chat_turn(user_uid, final_prompt)


PLAN_CHANGE_KEYWORDS = (
    "adjust",
    "change",
    "reschedule",
    "move",
    "shift",
    "update",
    "swap",
    "skip",
    "missed",
    "can't",
    "cant",
    "cannot",
    "won't",
    "wont",
    "unable",
    "reduce",
    "increase",
    "replace",
    "make ",
)

PLAN_REPLY_CHANGE_KEYWORDS = (
    "updated schedule",
    "updated plan",
    "adjusted schedule",
    "adjust your training week",
    "shift your remaining runs",
    "shifted",
    "rescheduled",
    "instead",
    "originally scheduled",
)


def _should_attempt_plan_update(user_message: str, assistant_reply: str) -> bool:
    request_text = (user_message or "").casefold()
    reply_text = (assistant_reply or "").casefold()
    return any(token in request_text for token in PLAN_CHANGE_KEYWORDS) or any(
        token in reply_text for token in PLAN_REPLY_CHANGE_KEYWORDS
    )


def _plan_patch_has_changes(patch: dict) -> bool:
    if not isinstance(patch, dict):
        return False
    try:
        if float(patch.get("scale_week_pct") or 0) != 0:
            return True
    except (TypeError, ValueError):
        pass
    workouts = patch.get("workouts")
    return isinstance(workouts, list) and any(isinstance(item, dict) and item.get("day_name") for item in workouts)


def _apply_plan_update_from_reply(
    user_uid: str,
    profile: dict,
    dashboard: dict | None,
    plan_context: str,
    user_message: str,
    assistant_reply: str,
) -> dict | None:
    if not dashboard or not _should_attempt_plan_update(user_message, assistant_reply):
        return None

    plan = dict(dashboard.get("plan") or {})
    plan_id = str(plan.get("id") or "").strip()
    week_id = str(dashboard.get("current_week_id") or "").strip()
    if not plan_id or not week_id:
        return None

    try:
        patch = generate_plan_patch(
            assistant_reply,
            plan_context,
            profile,
            user_message=user_message,
        )
        if not _plan_patch_has_changes(patch):
            return None
        result = apply_plan_patch(user_uid, plan_id, week_id, patch)
        st.session_state.plan_dashboard_dirty = True
        st.session_state.plan_update_notice = {
            "planned_km": result.get("planned_km"),
            "workout_count": result.get("workout_count"),
            "summary": result.get("adjustment_note") or patch.get("summary") or "Plan updated",
        }
        log_event(
            user_uid,
            "plan_adjustment_applied",
            {
                "session_id": st.session_state.get("active_session_id"),
                "planned_km": result.get("planned_km"),
                "workout_count": result.get("workout_count"),
            },
        )
        return result
    except Exception:
        st.session_state.plan_update_error = "I updated the reply, but could not sync the plan sidebar."
        log_event(
            user_uid,
            "plan_adjustment_apply_failed",
            {"session_id": st.session_state.get("active_session_id")},
        )
        return None


def _render_streaming_assistant_response(
    user_uid: str,
    profile: dict,
    *,
    dashboard: dict | None = None,
    plan_context: str = "",
) -> bool:
    sid = st.session_state.get("pending_assistant_session_id")
    if not sid or sid != st.session_state.get("active_session_id"):
        return False

    messages = st.session_state.get("pending_assistant_messages") or list(st.session_state.messages)
    latest_user_message = _latest_user_message(messages)
    rag_chunks = _retrieve_rag_chunks_for_message(latest_user_message)
    sources = collect_source_citations(rag_chunks, query=latest_user_message)
    reply = st.write_stream(
        stream_gemini_response(messages, profile, rag_chunks=rag_chunks, plan_context=plan_context)
    )
    if isinstance(reply, list):
        reply = "".join(str(part) for part in reply)
    reply = str(reply or "").strip()
    sources = _sources_for_reply(reply, sources)

    assistant_message = {"role": "assistant", "content": reply}
    if sources:
        assistant_message["sources"] = sources
        _render_message_sources(sources, key="msg_sources_streaming")

    st.session_state.messages.append(assistant_message)
    save_message_to_firestore(user_uid, sid, "assistant", reply, sources=sources)
    log_event(
        user_uid,
        "gemini_response_completed",
        {
            "session_id": sid,
            "reply_length": len(reply),
            "source_count": len(sources),
        },
    )
    _apply_plan_update_from_reply(user_uid, profile, dashboard, plan_context, latest_user_message, reply)
    st.session_state.pending_assistant_session_id = None
    st.session_state.pending_assistant_messages = []
    return True


def _format_message_content(content: str, *, role: str) -> str:
    text = (content or "").replace("\r\n", "\n").strip()
    if role == "user":
        return html.escape(text)
    return text


def _format_assistant_html(content: str) -> str:
    text = (content or "").replace("\r\n", "\n").strip()
    if not text:
        return ""

    paragraphs = [block.strip() for block in text.split("\n\n") if block.strip()]
    return "".join(
        f"<p>{_render_safe_inline_markdown(block).replace(chr(10), '<br>')}</p>"
        for block in paragraphs
    )


def _render_safe_inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def _retrieve_rag_chunks_for_message(user_message: str) -> list[dict]:
    if not user_message:
        return []

    try:
        return retrieve_context(user_message, top_k=5)
    except Exception:
        return []


def _source_initials(source: dict) -> str:
    title = str(source.get("title") or "Source")
    skip_words = {"a", "an", "and", "for", "in", "of", "on", "the", "to", "with"}
    words = [
        word
        for word in html.unescape(title).replace("-", " ").split()
        if word and word.casefold() not in skip_words
    ]
    if not words:
        return "S"
    if len(words) == 1:
        return words[0][:2].upper()
    return "".join(word[0].upper() for word in words[:2])


def _message_sources(message: dict) -> list[dict]:
    sources = message.get("sources")
    return sources if isinstance(sources, list) else []


def _sources_for_reply(reply: str, sources: list[dict]) -> list[dict]:
    if not sources:
        return []

    text = (reply or "").strip().casefold()
    if not text:
        return []

    no_source_prefixes = (
        "paceup hit the current gemini usage limit",
        "sorry, paceup could not reach gemini",
        "sorry, gemini_api_key is not configured",
        "i can't help with requests to reveal or override",
    )
    if any(text.startswith(prefix) for prefix in no_source_prefixes):
        return []

    return sources


def _render_message_sources(sources: list[dict], *, key: str) -> None:
    if not sources:
        return

    with st.container(key=key):
        with st.popover("Sources", key=f"{key}_popover", width="content"):
            source_rows = []
            for source in sources:
                title = html.escape(str(source.get("title") or "Untitled source"))
                url = html.escape(str(source.get("url") or ""), quote=True)
                year = html.escape(str(source.get("year") or ""))
                source_type = html.escape(str(source.get("source_type") or ""))
                heading = html.escape(str(source.get("heading") or ""))
                initials = html.escape(_source_initials(source))
                title_html = (
                    f'<a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>'
                    if url
                    else title
                )
                meta = " | ".join(part for part in (year, source_type) if part)
                source_rows.append(
                    '<div class="source-row">'
                    f'<div class="source-avatar">{initials}</div>'
                    '<div class="source-copy">'
                    f'<div class="source-title">{title_html}</div>'
                    f'<div class="source-meta">{meta}</div>'
                    f'<div class="source-heading">{heading}</div>'
                    '</div>'
                    '</div>'
                )
            source_panel_html = (
                '<div class="source-popover-panel">'
                '<div class="source-popover-title">Sources used</div>'
                f'{"".join(source_rows)}'
                '</div>'
            )
            st.markdown(source_panel_html, unsafe_allow_html=True)


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


def _coerce_date_value(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None


def _format_goal_date(value) -> str:
    goal_date = _coerce_date_value(value)
    if not goal_date:
        return "Race date not set"
    return f"{goal_date:%a} - {goal_date:%b} {goal_date.day}, {goal_date.year}"


def _days_until(value) -> int | None:
    goal_date = _coerce_date_value(value)
    if not goal_date:
        return None
    return max(0, (goal_date - date.today()).days)


def _format_km(value) -> str:
    try:
        numeric = float(value or 0)
    except (TypeError, ValueError):
        numeric = 0
    return f"{numeric:g}"


def _metric_value(value, fallback: str = "0") -> str:
    if value is None:
        return fallback
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{numeric:g}"


def _format_duration(seconds) -> str:
    try:
        total_seconds = int(seconds or 0)
    except (TypeError, ValueError):
        total_seconds = 0
    if total_seconds <= 0:
        return "--"
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def _format_pace_from_seconds(seconds) -> str:
    try:
        total_seconds = int(seconds or 0)
    except (TypeError, ValueError):
        total_seconds = 0
    if total_seconds <= 0:
        return "--"
    minutes, secs = divmod(total_seconds, 60)
    return f"{minutes}:{secs:02d}/km"


def _session_suffix(session_id: str | None) -> str:
    suffix = (session_id or "").replace("-", "")[-4:].upper()
    return suffix or "0001"


def _goal_title(profile: dict, summary: dict) -> str:
    configured = str(
        profile.get("goal_race_name")
        or profile.get("race_name")
        or profile.get("goal_event")
        or ""
    ).strip()
    if configured:
        return configured

    goal_distance = str(summary.get("goal_distance") or profile.get("goal_distance") or "Goal Race")
    if goal_distance.casefold() == "full marathon":
        return "Marathon Goal"
    return f"{goal_distance} Goal"


def _phase_label(summary: dict) -> str:
    focus = str(summary.get("week_focus") or "Build").strip()
    return focus.split()[0] if focus else "Build"


def _sorted_workouts(workouts: list[dict]) -> list[dict]:
    return sorted(workouts, key=lambda item: int(item.get("day_index") or 0))


def _workout_type(workout: dict) -> str:
    return str(workout.get("workout_type") or "easy").strip().lower()


def _workout_status(workout: dict) -> str:
    return str(workout.get("status") or "planned").strip().lower()


def _is_run_session(workout: dict) -> bool:
    if _workout_type(workout) == "rest":
        return False
    try:
        distance = float(workout.get("distance_km") or 0)
    except (TypeError, ValueError):
        distance = 0.0
    return distance > 0


def _is_upcoming_run(workout: dict) -> bool:
    return _is_run_session(workout) and _workout_status(workout) not in {"completed", "modified", "skipped"}


def _type_label(workout: dict) -> str:
    return {
        "easy": "Easy",
        "quality": "Workout",
        "long_run": "Long",
        "recovery": "Recovery",
        "rest": "Rest",
        "cross_train": "Cross",
    }.get(_workout_type(workout), _workout_type(workout).replace("_", " ").title())


def _day_short(workout: dict) -> str:
    return str(workout.get("day_name") or "?")[:3].title()


def _first_run_workout(workouts: list[dict]) -> dict:
    return next((item for item in _sorted_workouts(workouts) if _is_run_session(item)), {})


def _workout_detail(workout: dict) -> str:
    if not _is_run_session(workout):
        return "No running"
    distance = _format_km(workout.get("distance_km"))
    status = _workout_status(workout)
    actual_distance = workout.get("actual_distance_km")
    if status in {"completed", "modified"} and actual_distance is not None:
        actual = _format_km(actual_distance)
        if actual != distance:
            return f"{actual} km done / planned {distance} km"
        return f"{actual} km done"
    duration = _metric_value(workout.get("duration_min"), "")
    if duration:
        return f"{distance} km / {duration} min"
    return f"{distance} km"


def _rail_projection_rows(items: list[dict], *, limit: int = 6) -> str:
    values = [float(item.get("value") or 0) for item in items[:limit]]
    max_value = max(values or [1])
    rows = []
    for item, value in zip(items[:limit], values):
        label = html.escape(str(item.get("label") or "Week"))
        width = max(8, min(100, int(round((value / max_value) * 100)))) if max_value else 8
        rows.append(
            '<div class="rail-trend-row">'
            f"<span>{label}</span>"
            '<div class="rail-trend-track">'
            f'<i style="width: {width}%"></i>'
            "</div>"
            f"<strong>{html.escape(_format_km(value))}</strong>"
            "</div>"
        )
    return "".join(rows)


def _rail_workout_rows(workouts: list[dict], first_run: dict) -> str:
    rows = []
    first_run_key = (first_run.get("id"), first_run.get("day_name"))
    for workout in _sorted_workouts(workouts):
        workout_type = _workout_type(workout)
        status = _workout_status(workout)
        is_first = (workout.get("id"), workout.get("day_name")) == first_run_key
        first_badge = '<span class="rail-week-badge">First run</span>' if is_first and workout_type == "recovery" else ""
        classes = f"rail-week-row rail-type-{html.escape(workout_type)} rail-status-{html.escape(status)}"
        title = html.escape(str(workout.get("title") or _type_label(workout)))
        rows.append(
            f'<div class="{classes}">'
            f'<div class="rail-week-day">{html.escape(_day_short(workout))}</div>'
            '<div class="rail-week-main">'
            f"<strong>{title}</strong>"
            f"<span>{html.escape(_workout_detail(workout))}</span>"
            "</div>"
            '<div class="rail-week-tags">'
            f'<em>{html.escape(_type_label(workout))}</em>'
            f"{first_badge}"
            "</div>"
            "</div>"
        )
    return "".join(rows)


def _up_next_workout(dashboard: dict | None) -> dict:
    workouts = list((dashboard or {}).get("current_workouts") or [])
    if not workouts:
        return {}

    today = date.today()

    def sort_key(item: dict) -> tuple[int, int]:
        scheduled = _coerce_date_value(item.get("scheduled_date"))
        is_past = 1 if scheduled and scheduled < today else 0
        return (is_past, int(item.get("day_index") or 0))

    planned = [workout for workout in workouts if _is_upcoming_run(workout)]
    if not planned:
        return {}
    return sorted(planned, key=sort_key)[0]


def _workout_option_label(workout: dict) -> str:
    day = str(workout.get("day_name") or "Run")
    title = str(workout.get("title") or _type_label(workout))
    detail = _workout_detail(workout)
    return f"{day} - {title} ({detail})"


def _suggest_workout_match(workouts: list[dict], result: dict) -> str:
    run_workouts = [workout for workout in _sorted_workouts(workouts) if _is_run_session(workout)]
    if not run_workouts:
        return ""
    result_date = _coerce_date_value(result.get("run_date")) or date.today()
    if result_date:
        for workout in run_workouts:
            if _coerce_date_value(workout.get("scheduled_date")) == result_date:
                return str(workout.get("id") or "")
    result_distance = result.get("distance_km")
    try:
        result_km = float(result_distance or 0)
    except (TypeError, ValueError):
        result_km = 0
    if result_km > 0:
        return str(
            min(
                run_workouts,
                key=lambda item: abs(float(item.get("distance_km") or 0) - result_km),
            ).get("id")
            or ""
        )
    return str(run_workouts[0].get("id") or "")


def _run_result_widget_key(result: dict) -> str:
    raw = "_".join(
        str(part or "")
        for part in (
            result.get("run_date") or "today",
            result.get("distance_km"),
            result.get("duration_seconds") or result.get("moving_time_seconds"),
        )
    )
    return re.sub(r"[^A-Za-z0-9_]+", "_", raw).strip("_")[:80] or "latest"


def _run_result_summary_html(result: dict) -> str:
    confidence = result.get("confidence")
    try:
        confidence_pct = int(round(float(confidence or 0) * 100))
    except (TypeError, ValueError):
        confidence_pct = 0
    rows = [
        ("Distance", f"{_format_km(result.get('distance_km'))} km" if result.get("distance_km") is not None else "--"),
        ("Time", _format_duration(result.get("moving_time_seconds") or result.get("duration_seconds"))),
        ("Pace", _format_pace_from_seconds(result.get("average_pace_sec_per_km"))),
        ("Avg HR", f"{_metric_value(result.get('average_heart_rate_bpm'), '--')} bpm"),
    ]
    row_html = "".join(
        f"<div><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong></div>"
        for label, value in rows
    )
    source = result.get("source_app") or "Screenshot"
    summary = result.get("summary") or "Confirm the extracted metrics before saving."
    return (
        '<div class="run-result-card">'
        '<div class="run-result-top">'
        f"<span>{html.escape(str(source))}</span>"
        f"<em>{confidence_pct}% confidence</em>"
        "</div>"
        f'<p>{html.escape(str(summary))}</p>'
        f'<div class="run-result-grid">{row_html}</div>'
        '<div class="run-privacy-note">Map and location data ignored. Screenshot image is not stored.</div>'
        "</div>"
    )


def _ensure_chat_session_for_action(user_uid: str, seed_prompt: str) -> str:
    if not st.session_state.active_session_id:
        sid = create_chat_session(user_uid, seed_prompt)
        st.session_state.active_session_id = sid
        st.session_state.active_chat_id = sid
        st.session_state.chat_sessions = load_chat_sessions(user_uid)
    return st.session_state.active_session_id


def _append_chat_message(user_uid: str, role: str, content: str) -> None:
    sid = _ensure_chat_session_for_action(user_uid, content)
    message = {"role": role, "content": content}
    st.session_state.messages.append(message)
    save_message_to_firestore(user_uid, sid, role, content)


def _chat_input_text(value) -> str:
    if isinstance(value, str):
        return value.strip()
    try:
        return str(value.text or "").strip()
    except AttributeError:
        if isinstance(value, dict):
            return str(value.get("text") or "").strip()
    return ""


def _chat_input_files(value) -> list:
    if isinstance(value, str):
        return []
    try:
        return list(value.files or [])
    except AttributeError:
        if isinstance(value, dict):
            return list(value.get("files") or [])
    return []


def _handle_run_screenshot_chat_submission(user_uid: str, uploaded_file, note: str) -> None:
    if uploaded_file is None:
        return

    user_note = note or "Uploaded a post-run screenshot."
    _append_chat_message(
        user_uid,
        "user",
        f"{user_note}\n\n[Post-run screenshot attached. PaceUp will ignore map/location data.]",
    )
    try:
        with st.spinner("Reading run metrics from the screenshot..."):
            result = analyze_run_screenshot(
                uploaded_file.getvalue(),
                getattr(uploaded_file, "type", "") or "image/png",
            )
        st.session_state.run_screenshot_result = result
        st.session_state.run_screenshot_error = ""
        st.session_state.run_screenshot_saved_notice = ""
        log_event(user_uid, "run_screenshot_analyzed", {"confidence": result.get("confidence"), "surface": "chat_input"})
    except Exception as exc:
        st.session_state.run_screenshot_result = None
        st.session_state.run_screenshot_error = str(exc)
        st.session_state.run_screenshot_saved_notice = ""


def _render_run_screenshot_confirmation(user_uid: str, dashboard: dict | None) -> None:
    if not dashboard:
        return
    plan = dict(dashboard.get("plan") or {})
    plan_id = str(plan.get("id") or "")
    week_id = str(dashboard.get("current_week_id") or "")
    if not plan_id or not week_id:
        return

    workouts = [workout for workout in dashboard.get("current_workouts") or [] if _is_run_session(workout)]
    should_render = any(
        [
            st.session_state.get("run_screenshot_error"),
            st.session_state.get("run_screenshot_result"),
        ]
    )
    if not should_render:
        return

    with st.container(key="chat_run_screenshot_review"):
        if st.session_state.get("run_screenshot_error"):
            st.markdown(
                f'<div class="chat-run-status chat-run-error">{html.escape(st.session_state.run_screenshot_error)}</div>',
                unsafe_allow_html=True,
            )

        result = st.session_state.get("run_screenshot_result")
        if result:
            st.markdown(
                '<div class="chat-run-review-title">Review uploaded run</div>',
                unsafe_allow_html=True,
            )
            st.markdown(_run_result_summary_html(result), unsafe_allow_html=True)
            workout_options = [("__auto__", "Auto-match today's planned run")] + [
                (str(workout.get("id") or ""), _workout_option_label(workout)) for workout in workouts
            ] + [("", "Save as unplanned run")]
            suggested_id = _suggest_workout_match(workouts, result)
            option_ids = [item[0] for item in workout_options]
            default_index = option_ids.index(suggested_id) if suggested_id in option_ids else 0
            selected_label = st.selectbox(
                "Match to planned run",
                options=[item[1] for item in workout_options],
                index=default_index,
                key=f"run_screenshot_workout_match_label_{_run_result_widget_key(result)}",
            )
            selected_index = [item[1] for item in workout_options].index(selected_label)
            selected_option_id = workout_options[selected_index][0]
            selected_workout_id = "" if selected_option_id == "__auto__" else selected_option_id
            auto_match_run = selected_option_id == "__auto__"
            save_col, discard_col = st.columns(2)
            with save_col:
                if st.button("Save run", key="btn_save_run_screenshot", type="primary", use_container_width=True):
                    try:
                        saved = save_run_progress_entry(
                            user_uid,
                            plan_id,
                            week_id,
                            result,
                            workout_id=selected_workout_id,
                            auto_match=auto_match_run,
                        )
                        st.session_state.run_screenshot_result = None
                        st.session_state.run_screenshot_error = ""
                        matched_status = saved.get("matched_workout_status")
                        st.session_state.run_screenshot_saved_notice = ""
                        st.session_state.plan_dashboard_dirty = True
                        saved_distance = _format_km(saved.get("distance_km"))
                        assistant_save_note = (
                            f"Saved your {saved_distance} km run and updated the matching planned workout, so Up Next should move forward."
                            if matched_status != "unplanned"
                            else f"Saved your {saved_distance} km run as an unplanned entry. I ignored map/location data and did not store the screenshot image."
                        )
                        _append_chat_message(
                            user_uid,
                            "assistant",
                            assistant_save_note,
                        )
                        log_event(user_uid, "run_screenshot_saved", {"entry_id": saved.get("id")})
                        st.rerun()
                    except Exception as exc:
                        st.session_state.run_screenshot_error = f"Could not save run: {exc}"
                        st.rerun()
            with discard_col:
                if st.button("Discard", key="btn_discard_run_screenshot", use_container_width=True):
                    st.session_state.run_screenshot_result = None
                    st.session_state.run_screenshot_error = ""
                    st.session_state.run_screenshot_saved_notice = ""
                    st.rerun()


def _mark_workout_done(user_uid: str, plan_id: str, week_id: str, workout_id: str) -> None:
    if not plan_id or not week_id or not workout_id:
        return
    try:
        update_workout_status(user_uid, plan_id, week_id, workout_id, status="completed")
    except Exception:
        st.session_state.rail_status_error = "Could not update workout status."


def _render_context_rail(user_uid: str, profile: dict, dashboard: dict | None) -> None:
    summary = dict((dashboard or {}).get("summary") or {})
    plan = dict((dashboard or {}).get("plan") or {})
    current_week = dict((dashboard or {}).get("current_week") or {})
    workouts = list((dashboard or {}).get("current_workouts") or [])
    pace_zones = list((dashboard or {}).get("pace_zones") or [])
    weekly_projection = list((dashboard or {}).get("weekly_projection") or [])
    readiness_summary = dict((dashboard or {}).get("readiness_summary") or {})
    run_entries = list((dashboard or {}).get("run_entries") or [])
    goal_date = summary.get("goal_race_date") or profile.get("goal_race_date") or plan.get("goal_race_date")
    days_left = _days_until(goal_date)
    weeks_left = None if days_left is None else max(0, days_left // 7)
    plan_weeks = len((dashboard or {}).get("weeks") or []) or 6
    run_workouts = [workout for workout in workouts if _is_run_session(workout)]
    completed_runs = [workout for workout in run_workouts if _workout_status(workout) in {"completed", "modified"}]
    actual_week_km = summary.get("actual_week_km")
    remaining_km = sum(
        float(workout.get("distance_km") or 0)
        for workout in run_workouts
        if _workout_status(workout) not in {"completed", "modified", "skipped"}
    )
    completion_pct = int(round((len(completed_runs) / len(run_workouts)) * 100)) if run_workouts else 0
    first_run = _first_run_workout(workouts)
    first_run_is_recovery = bool(first_run and _workout_type(first_run) == "recovery")
    next_workout = _up_next_workout(dashboard)
    next_distance = _format_km(next_workout.get("distance_km")) if next_workout else ""
    next_title = str(next_workout.get("title") or "All runs logged")
    next_day = str(next_workout.get("day_name") or "This week")
    next_type = _type_label(next_workout) if next_workout else "Done"
    next_note = str(
        next_workout.get("description")
        if next_workout
        else "No remaining planned runs. Keep recovery easy and wait for the next scheduled session."
    )
    adjustment_note = str(current_week.get("adjustment_note") or "").strip()
    update_notice = dict(st.session_state.get("plan_update_notice") or {})
    update_error = st.session_state.pop("plan_update_error", "")
    zone_widths = [34, 52, 68, 86]

    if not pace_zones:
        pace_zones = [
            {"label": "Easy", "value": "--"},
            {"label": "Marathon", "value": "--"},
            {"label": "Thresh.", "value": "--"},
            {"label": "Interval", "value": "--"},
        ]

    zone_rows = []
    for index, zone in enumerate(pace_zones[:4]):
        label = html.escape(str(zone.get("label") or "Zone"))
        value = html.escape(str(zone.get("value") or "--"))
        width = zone_widths[min(index, len(zone_widths) - 1)]
        zone_rows.append(
            '<div class="rail-zone-row">'
            f'<span>{label}</span>'
            '<div class="rail-zone-track">'
            f'<i style="width: {width}%"></i>'
            '</div>'
            f'<strong>{value}</strong>'
            '</div>'
        )

    sync_card = ""
    if update_notice:
        sync_summary = html.escape(str(update_notice.get("summary") or "Plan synced from chat."))
        sync_card = (
            '<div class="rail-sync-card">'
            '<span>Plan synced</span>'
            f"<p>{sync_summary}</p>"
            "</div>"
        )

    error_card = ""
    if update_error:
        error_card = f'<div class="rail-status-error">{html.escape(update_error)}</div>'

    first_run_card = ""
    if first_run_is_recovery:
        first_run_card = (
            '<div class="rail-recovery-card">'
            '<span>First run is recovery</span>'
            "<p>This week opens easy on purpose. Keep it light and use it to absorb the adjustment.</p>"
            "</div>"
        )

    adjustment_card = ""
    if adjustment_note:
        adjustment_card = (
            '<div class="rail-note-card">'
            '<span>Latest adjustment</span>'
            f"<p>{html.escape(adjustment_note)}</p>"
            "</div>"
        )

    latest_run_card = ""
    if run_entries:
        latest_run = dict(run_entries[0])
        latest_date = latest_run.get("run_date") or "Recent"
        latest_distance = _format_km(latest_run.get("distance_km"))
        latest_pace = _format_pace_from_seconds(latest_run.get("average_pace_sec_per_km"))
        latest_hr = _metric_value(latest_run.get("average_heart_rate_bpm"), "--")
        latest_run_card = (
            '<div class="rail-latest-run-card">'
            '<span>Latest uploaded run</span>'
            f"<strong>{html.escape(str(latest_distance))} km</strong>"
            f"<p>{html.escape(str(latest_date))} | {html.escape(latest_pace)} | HR {html.escape(str(latest_hr))}</p>"
            '<em>Map ignored</em>'
            "</div>"
        )

    readiness_score = readiness_summary.get("score")
    readiness_label = str(readiness_summary.get("label") or "Readiness")
    readiness_detail = str(readiness_summary.get("detail") or "No check-in yet.")
    readiness_value = _metric_value(readiness_score, "--")
    week_rows = _rail_workout_rows(workouts, first_run) if workouts else '<div class="rail-empty-note">No workouts planned yet.</div>'
    trend_rows = _rail_projection_rows(weekly_projection) if weekly_projection else '<div class="rail-empty-note">No mileage plan yet.</div>'

    rail_html = "".join(
        [
            '<div class="coach-rail-copy">',
            '<div class="rail-title-row"><span>Training Snapshot</span><span>Live plan</span></div>',
            '<div class="rail-goal-card rail-hero-card">',
            '<div>',
            f"<h3>{html.escape(_goal_title(profile, summary))}</h3>",
            f"<p>{html.escape(_format_goal_date(goal_date))}</p>",
            "</div>",
            '<div class="rail-deadline-grid">',
            f'<div><strong>{html.escape(_metric_value(days_left, "--"))}</strong><span>days</span></div>',
            f'<div><strong>{html.escape(_metric_value(weeks_left, "--"))}</strong><span>to race</span></div>',
            f"<div><strong>{plan_weeks}</strong><span>plan weeks</span></div>",
            "</div></div>",
            sync_card,
            error_card,
            first_run_card,
            '<div class="rail-section-label">Week Control</div>',
            '<div class="rail-metric-grid">',
            f'<div><span>Volume</span><strong>{html.escape(_format_km(summary.get("current_week_km")))}<em>km</em></strong></div>',
            f'<div><span>Actual</span><strong>{html.escape(_format_km(actual_week_km))}<em>km</em></strong></div>',
            f'<div><span>Remaining</span><strong>{html.escape(_format_km(remaining_km))}<em>km</em></strong></div>',
            f"<div><span>Done</span><strong>{completion_pct}<em>%</em></strong></div>",
            "</div>",
            latest_run_card,
            '<div class="rail-section-label">Up Next</div>',
            '<div class="rail-upnext-card">',
            f'<div class="rail-upnext-top"><span>{html.escape(next_day)}</span><em>{html.escape(next_type)}</em></div>',
            f"<h4>{html.escape(next_title)}</h4>",
            f"<p>{html.escape(next_distance + ' km. ' if next_distance else '')}{html.escape(next_note)}</p>",
            "</div>",
            '<div class="rail-section-label">Week Plan</div>',
            f'<div class="rail-week-list">{week_rows}</div>',
            adjustment_card,
            '<div class="rail-section-label">Weekly Mileage</div>',
            f'<div class="rail-trend-list">{trend_rows}</div>',
            '<div class="rail-section-label">Readiness</div>',
            '<div class="rail-readiness-card">',
            f"<strong>{html.escape(readiness_value)}</strong>",
            "<div>",
            f"<span>{html.escape(readiness_label)}</span>",
            f"<p>{html.escape(readiness_detail)}</p>",
            "</div></div>",
            '<div class="rail-title-row rail-pace-title"><span>Pace Cues</span><span>Recalc</span></div>',
            f'<div class="rail-zone-list">{"".join(zone_rows)}</div>',
            "</div>",
        ]
    )
    st.markdown(rail_html, unsafe_allow_html=True)

    if next_workout and dashboard and _is_upcoming_run(next_workout):
        with st.container(key="coach_rail_done"):
            st.button(
                "Mark as done",
                key="btn_rail_mark_done",
                use_container_width=True,
                on_click=_mark_workout_done,
                args=(
                    user_uid,
                    str(plan.get("id") or ""),
                    str((dashboard or {}).get("current_week_id") or ""),
                    str(next_workout.get("id") or ""),
                ),
            )
    if st.session_state.pop("rail_status_error", ""):
        st.markdown(
            '<div class="rail-status-error">Could not update workout status.</div>',
            unsafe_allow_html=True,
        )


def show_chat() -> None:
    user = st.session_state.user
    profile = _get_cached_chat_profile(user)
    if _should_show_name_prompt(profile):
        _preferred_name_dialog(user.uid, _profile_display_name(user, profile))

    dashboard = None
    plan_context = ""
    try:
        dashboard = get_plan_dashboard(user.uid, profile)
        plan_context = build_plan_context(dashboard)
    except Exception:
        plan_context = ""

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
        sidebar_col, main_col, rail_col = st.columns([0.13, 0.72, 0.15], gap="small")

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
                                with st.container(key=f"sess_row_{session_id}"):
                                    btn_col, menu_col = st.columns([0.82, 0.18], gap="small")
                                    with btn_col:
                                        st.button(
                                            title,
                                            key=f"sess_{session_id}",
                                            type="primary" if is_active else "secondary",
                                            use_container_width=True,
                                            on_click=_open_chat_session,
                                            args=(user.uid, session_id),
                                        )
                                    with menu_col:
                                        if st.button(
                                            "...",
                                            key=f"menu_{session_id}",
                                            use_container_width=True,
                                        ):
                                            st.session_state.editing_session_id = session_id
                                            st.session_state.editing_session_title = title
                                            st.rerun()

                editing_id = st.session_state.get("editing_session_id")
                if editing_id:
                    _edit_conversation_dialog(
                        user.uid,
                        editing_id,
                        st.session_state.get("editing_session_title", ""),
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
                    header_sub = (
                        f"{active_session_title} - session #{_session_suffix(st.session_state.active_session_id)}"
                        if active_session_title
                        else f"{goal} coaching - live session"
                    )
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
                                <span class="chat-header-icon" title="Share">&#8599;</span>
                                <span class="chat-header-icon" title="More">&#8230;</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with st.container(key="chat_body", height="stretch", border=False):
                    with st.container(key="chat_body_inner"):
                        suggestion_slot = st.empty()
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
                            with suggestion_slot.container():
                                _render_suggestion_chips(user.uid)
                        else:
                            suggestion_slot.empty()
                            streamed_reply_finished = False
                            display_messages = _messages_for_display(st.session_state.messages, active_session_title)
                            if st.session_state.get("chat_has_more_messages"):
                                st.button(
                                    "Load older messages",
                                    key="btn_load_older_messages",
                                    use_container_width=False,
                                    on_click=_load_older_messages,
                                    args=(user.uid, st.session_state.active_session_id),
                                )

                            for message_index, msg in enumerate(display_messages):
                                role = msg["role"]
                                content = msg["content"]
                                is_user = role == "user"
                                if is_user:
                                    formatted_content = _format_message_content(content, role=role)
                                    st.markdown(
                                        f"""<div class="chat-msg user-msg"><div class="msg-inner"><div class="msg-bubble">{formatted_content}</div></div><div class="msg-avatar user-avatar-sm">{html.escape(initials)}</div></div>""",
                                        unsafe_allow_html=True,
                                    )
                                else:
                                    formatted_content = _format_assistant_html(content)
                                    st.markdown(
                                        f'<div class="chat-msg assistant-msg"><div class="msg-avatar coach-avatar-sm">P</div><div class="msg-inner"><div class="assistant-response">{formatted_content}</div></div></div>',
                                        unsafe_allow_html=True,
                                    )
                                    _render_message_sources(
                                        _message_sources(msg),
                                        key=f"msg_sources_{message_index}",
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
                                            streamed_reply_finished = _render_streaming_assistant_response(
                                                user.uid,
                                                profile,
                                                dashboard=dashboard,
                                                plan_context=plan_context,
                                            )
                            if streamed_reply_finished:
                                st.session_state.chat_sessions = load_chat_sessions(user.uid)
                                if st.session_state.pop("plan_dashboard_dirty", False):
                                    try:
                                        dashboard = get_plan_dashboard(user.uid, profile)
                                        plan_context = build_plan_context(dashboard)
                                    except Exception:
                                        plan_context = ""
                        _render_run_screenshot_confirmation(user.uid, dashboard)
        with rail_col:
            with st.container(key="chat_context_rail"):
                _render_context_rail(user.uid, profile, dashboard)
    prompt = st.chat_input(
        "Ask PaceUp anything - attach a run screenshot here too...",
        key="chat_input_prompt",
        accept_file=True,
        file_type=["png", "jpg", "jpeg", "webp"],
    )
    if prompt:
        prompt_text = _chat_input_text(prompt)
        prompt_files = _chat_input_files(prompt)
        if prompt_files:
            _handle_run_screenshot_chat_submission(user.uid, prompt_files[0], prompt_text)
        elif prompt_text:
            _submit_chat_turn(user.uid, prompt_text, "typed")
        st.rerun()
