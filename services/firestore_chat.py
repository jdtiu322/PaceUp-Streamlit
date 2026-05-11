from __future__ import annotations

import logging
from datetime import datetime, timezone

from firebase_admin import firestore

from services.firebase import get_firestore_client


MESSAGE_PAGE_SIZE = 12
LATEST_MESSAGE_SNIPPET_LENGTH = 140
logger = logging.getLogger(__name__)


def _message_snippet(content: str, limit: int = LATEST_MESSAGE_SNIPPET_LENGTH) -> str:
    text = " ".join((content or "").split())
    return text[:limit] + ("..." if len(text) > limit else "")


def load_chat_sessions(uid: str) -> list:
    try:
        db = get_firestore_client()
        sessions_ref = (
            db
            .collection("users").document(uid)
            .collection("chat_sessions")
            .order_by("updated_at", direction=firestore.Query.DESCENDING)
            .stream()
        )
        sessions = []
        for doc in sessions_ref:
            data = doc.to_dict()
            data["id"] = doc.id
            sessions.append(data)
        return sessions
    except Exception:
        logger.exception("Failed to load chat sessions for user %s.", uid)
        return []


def create_chat_session(uid: str, first_message: str) -> str:
    title = first_message[:40] + ("..." if len(first_message) > 40 else "")
    now = datetime.now(timezone.utc)
    ref = (
        get_firestore_client()
        .collection("users").document(uid)
        .collection("chat_sessions")
        .add(
            {
                "title": title,
                "created_at": now,
                "updated_at": now,
                "latest_message_snippet": _message_snippet(first_message),
                "latest_message_role": "user",
                "latest_message_at": now,
            }
        )
    )
    return ref[1].id


def save_message_to_firestore(uid: str, session_id: str, role: str, content: str) -> None:
    now = datetime.now(timezone.utc)
    db = get_firestore_client()
    session_ref = db.collection("users").document(uid).collection("chat_sessions").document(session_id)
    message_ref = session_ref.collection("messages").document()
    batch = db.batch()
    batch.set(message_ref, {"role": role, "content": content, "timestamp": now})
    batch.update(
        session_ref,
        {
            "updated_at": now,
            "latest_message_snippet": _message_snippet(content),
            "latest_message_role": role,
            "latest_message_at": now,
        },
    )
    batch.commit()


def load_messages_for_session(uid: str, session_id: str) -> list:
    try:
        db = get_firestore_client()
        msgs_ref = (
            db
            .collection("users").document(uid)
            .collection("chat_sessions").document(session_id)
            .collection("messages")
            .order_by("timestamp")
            .stream()
        )
        return [{"role": msg.to_dict()["role"], "content": msg.to_dict()["content"]} for msg in msgs_ref]
    except Exception:
        logger.exception("Failed to load all messages for session %s/%s.", uid, session_id)
        return []


def load_recent_messages_page(uid: str, session_id: str, page_size: int = MESSAGE_PAGE_SIZE) -> tuple[list, str | None, bool]:
    try:
        db = get_firestore_client()
        msgs_ref = (
            db
            .collection("users").document(uid)
            .collection("chat_sessions").document(session_id)
            .collection("messages")
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .limit(page_size + 1)
            .stream()
        )

        docs = list(msgs_ref)
        has_more = len(docs) > page_size
        docs = docs[:page_size]
        docs.reverse()

        messages = [{"role": doc.to_dict()["role"], "content": doc.to_dict()["content"]} for doc in docs]
        cursor = docs[0].to_dict().get("timestamp").isoformat() if docs else None
        return messages, cursor, has_more
    except Exception:
        logger.exception("Failed to load recent messages page for session %s/%s.", uid, session_id)
        return [], None, False


def load_older_messages_page(
    uid: str, session_id: str, before_timestamp: str | None, page_size: int = MESSAGE_PAGE_SIZE
) -> tuple[list, str | None, bool]:
    if not before_timestamp:
        return [], before_timestamp, False

    try:
        cursor = datetime.fromisoformat(before_timestamp)
        db = get_firestore_client()
        msgs_ref = (
            db
            .collection("users").document(uid)
            .collection("chat_sessions").document(session_id)
            .collection("messages")
            .where("timestamp", "<", cursor)
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .limit(page_size + 1)
            .stream()
        )

        docs = list(msgs_ref)
        has_more = len(docs) > page_size
        docs = docs[:page_size]
        docs.reverse()

        messages = [{"role": doc.to_dict()["role"], "content": doc.to_dict()["content"]} for doc in docs]
        next_cursor = docs[0].to_dict().get("timestamp").isoformat() if docs else before_timestamp
        return messages, next_cursor, has_more
    except Exception:
        logger.exception("Failed to load older messages page for session %s/%s.", uid, session_id)
        return [], before_timestamp, False
