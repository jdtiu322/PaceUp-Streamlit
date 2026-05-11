from __future__ import annotations

import logging
from datetime import datetime, timezone

from services.firebase import get_firestore_client

logger = logging.getLogger(__name__)


def log_event(uid: str | None, name: str, properties: dict | None = None) -> None:
    if not uid:
        return

    try:
        get_firestore_client().collection("users").document(uid).collection("events").add(
            {
                "name": name,
                "properties": properties or {},
                "created_at": datetime.now(timezone.utc),
            }
        )
    except Exception:
        logger.exception("Failed to log telemetry event %s for user %s.", name, uid)
