from __future__ import annotations

import json
import logging
import re
from datetime import date

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL


logger = logging.getLogger(__name__)
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

RUN_SCREENSHOT_SCHEMA = """
{
  "is_run_summary": boolean,
  "source_app": string|null,
  "run_date": "YYYY-MM-DD"|null,
  "distance_km": number|null,
  "duration_seconds": integer|null,
  "moving_time_seconds": integer|null,
  "average_pace_sec_per_km": integer|null,
  "average_heart_rate_bpm": integer|null,
  "max_heart_rate_bpm": integer|null,
  "elevation_gain_m": number|null,
  "calories": integer|null,
  "splits": [{"label": string, "distance_km": number|null, "pace_sec_per_km": integer|null}],
  "confidence": number,
  "missing_fields": [string],
  "summary": string
}
"""


def _extract_json_object(raw_text: str) -> dict | None:
    text = (raw_text or "").strip()
    if not text:
        return None
    fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if fence_match:
        text = fence_match.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        parsed = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _coerce_float(value) -> float | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    return numeric if numeric >= 0 else None


def _coerce_int(value) -> int | None:
    try:
        numeric = int(round(float(value)))
    except (TypeError, ValueError):
        return None
    return numeric if numeric >= 0 else None


def _coerce_date(value) -> str | None:
    if not value:
        return None
    text = str(value).strip()[:10]
    try:
        return date.fromisoformat(text).isoformat()
    except ValueError:
        return None


def _normalize_result(result: dict) -> dict:
    splits = []
    for item in result.get("splits") or []:
        if not isinstance(item, dict):
            continue
        splits.append(
            {
                "label": str(item.get("label") or "").strip()[:40],
                "distance_km": _coerce_float(item.get("distance_km")),
                "pace_sec_per_km": _coerce_int(item.get("pace_sec_per_km")),
            }
        )

    confidence = _coerce_float(result.get("confidence"))
    confidence = max(0.0, min(1.0, confidence if confidence is not None else 0.0))
    missing_fields = result.get("missing_fields") if isinstance(result.get("missing_fields"), list) else []

    return {
        "is_run_summary": bool(result.get("is_run_summary", True)),
        "source_app": str(result.get("source_app") or "").strip()[:40] or None,
        "run_date": _coerce_date(result.get("run_date")),
        "distance_km": _coerce_float(result.get("distance_km")),
        "duration_seconds": _coerce_int(result.get("duration_seconds")),
        "moving_time_seconds": _coerce_int(result.get("moving_time_seconds")),
        "average_pace_sec_per_km": _coerce_int(result.get("average_pace_sec_per_km")),
        "average_heart_rate_bpm": _coerce_int(result.get("average_heart_rate_bpm")),
        "max_heart_rate_bpm": _coerce_int(result.get("max_heart_rate_bpm")),
        "elevation_gain_m": _coerce_float(result.get("elevation_gain_m")),
        "calories": _coerce_int(result.get("calories")),
        "splits": splits[:20],
        "confidence": confidence,
        "missing_fields": [str(item)[:40] for item in missing_fields[:12]],
        "summary": str(result.get("summary") or "").strip()[:240],
        "map_data_ignored": True,
        "image_stored": False,
    }


def analyze_run_screenshot(image_bytes: bytes, mime_type: str) -> dict:
    if client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    if not image_bytes:
        raise ValueError("Upload a screenshot first.")
    if mime_type not in {"image/png", "image/jpeg", "image/jpg", "image/webp"}:
        raise ValueError("Please upload a PNG, JPG, or WEBP screenshot.")

    prompt = f"""
You extract post-run summary metrics from a fitness app screenshot for PaceUp.

Privacy rule:
- Ignore maps, route traces, GPS paths, street names, start/end locations, exact coordinates, and any other location clues.
- Do not mention, infer, return, or store map/location data.
- Extract only workout metrics visible in the screenshot.

Return JSON only using this schema:
{RUN_SCREENSHOT_SCHEMA}

Rules:
- Prefer kilometers. Convert miles to kilometers if the screenshot uses miles.
- Prefer seconds for durations and pace.
- If a value is not clearly visible, use null and list it in missing_fields.
- confidence is 0 to 1 for how reliable the extraction is.
- summary should be one short sentence about the workout metrics, not location.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        config=types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=900,
            response_mime_type="application/json",
        ),
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                ],
            )
        ],
    )
    parsed = _extract_json_object(getattr(response, "text", "") or "")
    if not parsed:
        raise RuntimeError("Could not read run metrics from that screenshot.")
    normalized = _normalize_result(parsed)
    if not normalized["is_run_summary"]:
        raise RuntimeError("That image does not look like a post-run summary.")
    return normalized
