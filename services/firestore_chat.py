from __future__ import annotations

from datetime import datetime, timezone

from firebase_admin import firestore


def load_chat_sessions(uid: str) -> list:
    try:
        sessions_ref = (
            firestore.client()
            .collection("users").document(uid)
            .collection("chat_sessions")
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .limit(30)
            .stream()
        )
        sessions = []
        for doc in sessions_ref:
            data = doc.to_dict()
            data["id"] = doc.id
            sessions.append(data)
        return sessions
    except Exception:
        return []


def create_chat_session(uid: str, first_message: str) -> str:
    title = first_message[:40] + ("..." if len(first_message) > 40 else "")
    now = datetime.now(timezone.utc)
    ref = (
        firestore.client()
        .collection("users").document(uid)
        .collection("chat_sessions")
        .add({"title": title, "created_at": now, "updated_at": now})
    )
    return ref[1].id


def save_message_to_firestore(uid: str, session_id: str, role: str, content: str) -> None:
    now = datetime.now(timezone.utc)
    (
        firestore.client()
        .collection("users").document(uid)
        .collection("chat_sessions").document(session_id)
        .collection("messages")
        .add({"role": role, "content": content, "timestamp": now})
    )
    (
        firestore.client()
        .collection("users").document(uid)
        .collection("chat_sessions").document(session_id)
        .update({"updated_at": now})
    )


def load_messages_for_session(uid: str, session_id: str) -> list:
    try:
        msgs_ref = (
            firestore.client()
            .collection("users").document(uid)
            .collection("chat_sessions").document(session_id)
            .collection("messages")
            .order_by("timestamp")
            .stream()
        )
        return [{"role": msg.to_dict()["role"], "content": msg.to_dict()["content"]} for msg in msgs_ref]
    except Exception:
        return []
