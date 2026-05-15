from __future__ import annotations

import logging
import math
from collections import Counter
from datetime import date, datetime, timedelta, timezone

from firebase_admin import firestore

from services.firebase import get_firestore_client


logger = logging.getLogger(__name__)

DAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
DAY_INDEX = {day: index for index, day in enumerate(DAY_ORDER)}
DEFAULT_TRAINING_DAYS = ["Tuesday", "Thursday", "Sunday"]
PLAN_HORIZON_WEEKS = 6
WORKOUT_TYPE_LABELS = {
    "easy": "Easy",
    "quality": "Workout",
    "long_run": "Long run",
    "recovery": "Recovery",
    "rest": "Rest",
    "cross_train": "Cross-train",
}
WORKOUT_STATUS_LABELS = {
    "planned": "Planned",
    "completed": "Completed",
    "skipped": "Skipped",
    "modified": "Modified",
}
EFFORT_OPTIONS = ("Easy", "Moderate", "Hard")

GOAL_DEFAULTS = {
    "5K": {"base_weekly_km": 18.0, "long_run_share": 0.24, "long_run_cap": 14.0},
    "10K": {"base_weekly_km": 22.0, "long_run_share": 0.27, "long_run_cap": 18.0},
    "Half Marathon": {"base_weekly_km": 28.0, "long_run_share": 0.33, "long_run_cap": 26.0},
    "Full Marathon": {"base_weekly_km": 34.0, "long_run_share": 0.38, "long_run_cap": 34.0},
    "Ultra Marathon": {"base_weekly_km": 44.0, "long_run_share": 0.43, "long_run_cap": 45.0},
}
WEEKLY_PROGRESSION = [1.0, 1.08, 1.14, 0.92, 1.18, 1.24]


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _coerce_date(value) -> date | None:
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


def _goal_race_date_iso(source: dict) -> str | None:
    goal_date = _coerce_date((source or {}).get("goal_race_date"))
    return goal_date.isoformat() if goal_date else None


def current_week_start(today: date | None = None) -> date:
    current = today or date.today()
    return current - timedelta(days=current.weekday())


def week_id_for(week_start: date) -> str:
    return week_start.isoformat()


def _plan_collection(uid: str):
    return get_firestore_client().collection("users").document(uid).collection("plans")


def _user_ref(uid: str):
    return get_firestore_client().collection("users").document(uid)


def _week_ref(uid: str, plan_id: str, week_id: str):
    return _plan_collection(uid).document(plan_id).collection("weeks").document(week_id)


def _goal_defaults(profile: dict) -> dict:
    goal = str(profile.get("goal_distance") or "Full Marathon")
    return GOAL_DEFAULTS.get(goal, GOAL_DEFAULTS["Full Marathon"])


def _normalized_training_days(profile: dict) -> list[str]:
    training_days = [
        day for day in (profile.get("training_days") or []) if day in DAY_INDEX
    ]
    if not training_days:
        training_days = DEFAULT_TRAINING_DAYS[:]
    return sorted(training_days, key=DAY_INDEX.get)


def _current_weekly_km(profile: dict) -> float:
    raw = profile.get("current_weekly_km")
    try:
        value = float(raw)
    except (TypeError, ValueError):
        value = 0.0
    baseline = _goal_defaults(profile)["base_weekly_km"]
    return max(value, baseline * 0.6)


def _round_half(value: float) -> float:
    return round(value * 2) / 2


def _weekly_target(profile: dict, week_offset: int) -> float:
    baseline = max(_current_weekly_km(profile), 8.0)
    multiplier = WEEKLY_PROGRESSION[min(max(week_offset, 0), len(WEEKLY_PROGRESSION) - 1)]
    return _round_half(max(8.0, baseline * multiplier))


def _week_focus(week_offset: int) -> str:
    focuses = [
        "Build consistency",
        "Sharpen aerobic rhythm",
        "Layer in controlled quality",
        "Recovery absorb week",
        "Long-run confidence",
        "Race-specific momentum",
    ]
    return focuses[min(max(week_offset, 0), len(focuses) - 1)]


def _day_date(week_start: date, day_name: str) -> date:
    return week_start + timedelta(days=DAY_INDEX[day_name])


def _minutes_for_distance(distance_km: float, *, workout_type: str) -> int:
    pace_minutes = {
        "quality": 5.35,
        "long_run": 6.2,
        "recovery": 6.45,
        "easy": 6.05,
        "cross_train": 6.4,
        "rest": 0,
    }.get(workout_type, 6.05)
    if workout_type == "rest":
        return 0
    return int(round(max(distance_km * pace_minutes, 20)))


def _day_note(workout_type: str, *, week_offset: int) -> str:
    if workout_type == "quality":
        if week_offset >= 4:
            return "Controlled marathon-effort work. Finish feeling smooth, not cooked."
        return "Stay relaxed. This should feel purposeful, not all-out."
    if workout_type == "long_run":
        return "Easy conversational effort. Practice fueling and smooth pacing."
    if workout_type == "recovery":
        return "Very easy effort. Keep this one light and rhythmic."
    if workout_type == "rest":
        return "No running today. Mobility or a short walk is enough."
    return "Easy aerobic running. Keep the effort steady and controlled."


def _distribute_day_types(training_days: list[str], preferred_long_run_day: str) -> dict[str, str]:
    long_run_day = preferred_long_run_day if preferred_long_run_day in training_days else training_days[-1]
    remaining = [day for day in training_days if day != long_run_day]
    quality_day = remaining[0] if remaining else long_run_day
    types: dict[str, str] = {}
    for idx, day in enumerate(training_days):
        if day == long_run_day:
            types[day] = "long_run"
        elif day == quality_day and len(training_days) > 1:
            types[day] = "quality"
        elif len(training_days) >= 4 and idx == len(training_days) - 2:
            types[day] = "recovery"
        else:
            types[day] = "easy"
    return types


def _build_week_workouts(profile: dict, week_start: date, *, week_offset: int) -> list[dict]:
    training_days = _normalized_training_days(profile)
    defaults = _goal_defaults(profile)
    preferred_long_run_day = str(profile.get("preferred_long_run_day") or "Sunday")
    weekly_target = _weekly_target(profile, week_offset)
    day_types = _distribute_day_types(training_days, preferred_long_run_day)

    long_run_distance = min(
        defaults["long_run_cap"],
        max(6.0, _round_half(weekly_target * defaults["long_run_share"])),
    )
    quality_distance = _round_half(max(5.0, weekly_target * 0.24))
    remainder = max(0.0, weekly_target - long_run_distance - quality_distance)
    easy_days = [day for day in training_days if day_types.get(day) in {"easy", "recovery"}]
    easy_share = _round_half(remainder / max(len(easy_days), 1)) if easy_days else 0.0

    workouts: list[dict] = []
    for day in training_days:
        workout_type = day_types.get(day, "easy")
        if workout_type == "long_run":
            distance_km = long_run_distance
            title = "Long run"
        elif workout_type == "quality":
            distance_km = quality_distance
            title = "Workout session"
        else:
            distance_km = max(4.0, easy_share or weekly_target / max(len(training_days), 1))
            title = "Recovery run" if workout_type == "recovery" else "Easy run"

        workouts.append(
            {
                "day_name": day,
                "day_index": DAY_INDEX[day],
                "scheduled_date": _day_date(week_start, day).isoformat(),
                "workout_type": workout_type,
                "title": title,
                "description": _day_note(workout_type, week_offset=week_offset),
                "distance_km": _round_half(distance_km),
                "duration_min": _minutes_for_distance(distance_km, workout_type=workout_type),
                "effort_target": "Easy" if workout_type in {"easy", "recovery", "long_run"} else "Moderate",
                "status": "planned",
                "completion_effort": "",
                "actual_distance_km": None,
                "completion_note": "",
                "source": "seeded_plan",
            }
        )

    return workouts


def _build_week_payload(profile: dict, week_start: date, *, week_offset: int) -> tuple[dict, list[dict]]:
    workouts = _build_week_workouts(profile, week_start, week_offset=week_offset)
    planned_km = _round_half(sum(float(item.get("distance_km") or 0.0) for item in workouts))
    payload = {
        "start_date": week_start.isoformat(),
        "end_date": (week_start + timedelta(days=6)).isoformat(),
        "focus": _week_focus(week_offset),
        "planned_km": planned_km,
        "adjustment_note": "",
        "created_at": _now_utc(),
        "updated_at": _now_utc(),
    }
    return payload, workouts


def _create_plan_document(uid: str, profile: dict) -> dict:
    now = _now_utc()
    defaults = _goal_defaults(profile)
    ref = _plan_collection(uid).document()
    payload = {
        "status": "active",
        "goal_distance": profile.get("goal_distance"),
        "goal_race_date": _goal_race_date_iso(profile),
        "preferred_long_run_day": profile.get("preferred_long_run_day") or "Sunday",
        "target_weekly_km": _round_half(max(_current_weekly_km(profile), defaults["base_weekly_km"])),
        "created_at": now,
        "updated_at": now,
        "current_week_start": current_week_start().isoformat(),
        "source": "paceup_seeded",
    }
    ref.set(payload)
    _user_ref(uid).update({"active_plan_id": ref.id, "updated_at": now})
    payload["id"] = ref.id
    return payload


def _sync_plan_goal_fields(uid: str, plan: dict, profile: dict) -> dict:
    plan_id = str(plan.get("id") or "").strip()
    if not plan_id:
        return plan

    updates = {}
    goal_distance = profile.get("goal_distance")
    goal_race_date = _goal_race_date_iso(profile)
    preferred_long_run_day = profile.get("preferred_long_run_day")

    if goal_distance and plan.get("goal_distance") != goal_distance:
        updates["goal_distance"] = goal_distance
    if goal_race_date and _goal_race_date_iso(plan) != goal_race_date:
        updates["goal_race_date"] = goal_race_date
    if preferred_long_run_day and plan.get("preferred_long_run_day") != preferred_long_run_day:
        updates["preferred_long_run_day"] = preferred_long_run_day

    if not updates:
        return plan

    updates["updated_at"] = _now_utc()
    _plan_collection(uid).document(plan_id).update(updates)
    synced = dict(plan)
    synced.update(updates)
    return synced


def _load_plan(uid: str, plan_id: str) -> dict | None:
    doc = _plan_collection(uid).document(plan_id).get()
    if not doc.exists:
        return None
    data = doc.to_dict() or {}
    data["id"] = doc.id
    return data


def _ensure_week(uid: str, plan_id: str, profile: dict, week_start: date, *, week_offset: int) -> None:
    week_id = week_id_for(week_start)
    week_ref = _week_ref(uid, plan_id, week_id)
    week_doc = week_ref.get()
    if week_doc.exists:
        workouts = list(week_ref.collection("workouts").stream())
        if workouts:
            return
    payload, workouts = _build_week_payload(profile, week_start, week_offset=week_offset)
    batch = get_firestore_client().batch()
    batch.set(week_ref, payload, merge=True)
    for workout in workouts:
        workout_id = f"{workout['day_name'].lower()}_{workout['workout_type']}"
        batch.set(week_ref.collection("workouts").document(workout_id), workout, merge=True)
    batch.commit()


def ensure_active_plan(uid: str, profile: dict) -> dict:
    active_plan_id = str(profile.get("active_plan_id") or "").strip()
    plan = _load_plan(uid, active_plan_id) if active_plan_id else None
    if plan is None:
        plan = _create_plan_document(uid, profile)
        profile["active_plan_id"] = plan["id"]
    else:
        plan = _sync_plan_goal_fields(uid, plan, profile)

    week_start = current_week_start()
    for offset in range(PLAN_HORIZON_WEEKS):
        _ensure_week(uid, plan["id"], profile, week_start + timedelta(days=7 * offset), week_offset=offset)

    fresh = _load_plan(uid, plan["id"])
    return fresh or plan


def _load_weeks(uid: str, plan_id: str, *, start_date_value: date, limit: int = PLAN_HORIZON_WEEKS) -> list[dict]:
    docs = (
        _plan_collection(uid)
        .document(plan_id)
        .collection("weeks")
        .where("start_date", ">=", start_date_value.isoformat())
        .order_by("start_date")
        .limit(limit)
        .stream()
    )
    weeks: list[dict] = []
    for doc in docs:
        payload = doc.to_dict() or {}
        payload["id"] = doc.id
        weeks.append(payload)
    return weeks


def _load_workouts(uid: str, plan_id: str, week_id: str) -> list[dict]:
    docs = (
        _week_ref(uid, plan_id, week_id)
        .collection("workouts")
        .order_by("day_index")
        .stream()
    )
    workouts: list[dict] = []
    for doc in docs:
        payload = doc.to_dict() or {}
        payload["id"] = doc.id
        workouts.append(payload)
    return workouts


def _load_readiness_entries(uid: str, plan_id: str, *, limit: int = 8) -> list[dict]:
    docs = (
        _plan_collection(uid)
        .document(plan_id)
        .collection("readiness_entries")
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    entries: list[dict] = []
    for doc in docs:
        payload = doc.to_dict() or {}
        payload["id"] = doc.id
        entries.append(payload)
    return entries


def _load_run_entries(uid: str, plan_id: str, *, limit: int = 8) -> list[dict]:
    docs = (
        _plan_collection(uid)
        .document(plan_id)
        .collection("run_entries")
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    entries: list[dict] = []
    for doc in docs:
        payload = doc.to_dict() or {}
        payload["id"] = doc.id
        entries.append(payload)
    return entries


def _completion_rate(workouts: list[dict]) -> float:
    done = sum(1 for workout in workouts if _workout_status(workout) in {"completed", "modified"})
    total = len(workouts)
    return round((done / total) * 100, 1) if total else 0.0


def _latest_readiness_summary(entries: list[dict]) -> dict:
    if not entries:
        return {
            "label": "No check-in yet",
            "score": None,
            "detail": "Log sleep, soreness, energy, and motivation to adapt the week.",
        }
    latest = entries[0]
    score = latest.get("overall_score")
    detail = (
        f"Sleep {latest.get('sleep')}/5 · Energy {latest.get('energy')}/5 · "
        f"Soreness {latest.get('soreness')}/5"
    )
    return {
        "label": "Latest readiness",
        "score": score,
        "detail": detail,
    }


def _parse_recent_race_distance(recent_race_time: str) -> tuple[float, int] | None:
    if not recent_race_time:
        return None
    text = recent_race_time.strip().lower()
    if not text:
        return None
    distance_map = {
        "5k": 5.0,
        "10k": 10.0,
        "half marathon": 21.1,
        "marathon": 42.2,
        "full marathon": 42.2,
    }
    distance = None
    for label, value in distance_map.items():
        if label in text:
            distance = value
            break
    import re

    time_match = re.search(r"(?:(\d{1,2}):)?(\d{1,2}):(\d{2})", text)
    if time_match:
        hours = int(time_match.group(1) or 0)
        minutes = int(time_match.group(2))
        seconds = int(time_match.group(3))
        total_seconds = (hours * 3600) + (minutes * 60) + seconds
    else:
        compact_match = re.search(r"(\d+(?:\.\d+)?)\s*(h|hr|hrs|hours|min|mins|minutes)", text)
        if not compact_match:
            return None
        value = float(compact_match.group(1))
        unit = compact_match.group(2)
        total_seconds = int(round(value * 3600 if unit.startswith("h") else value * 60))

    if distance is None:
        distance = 5.0 if total_seconds < 45 * 60 else 10.0
    return distance, total_seconds


def _format_pace(minutes_per_km: float) -> str:
    total_seconds = int(round(minutes_per_km * 60))
    mins, secs = divmod(total_seconds, 60)
    return f"{mins}:{secs:02d}/km"


def _format_week_range_label(week: dict) -> str:
    start = _coerce_date(week.get("start_date"))
    end = _coerce_date(week.get("end_date")) or (start + timedelta(days=6) if start else None)
    if not start:
        return str(week.get("start_date") or "Week")
    if not end:
        return start.strftime("%b %d")
    if start.month == end.month:
        return f"{start:%b} {start.day}-{end.day}"
    return f"{start:%b} {start.day}-{end:%b} {end.day}"


def build_pace_zones(profile: dict) -> list[dict]:
    parsed = _parse_recent_race_distance(str(profile.get("recent_race_time") or ""))
    if not parsed:
        weekly_km = max(_current_weekly_km(profile), 20.0)
        base_pace = 6.4 - min(1.25, weekly_km / 80)
    else:
        distance_km, total_seconds = parsed
        race_pace = total_seconds / 60 / distance_km
        base_pace = race_pace

    zones = [
        ("Easy", base_pace * 1.20),
        ("Marathon", base_pace * 1.10),
        ("Threshold", base_pace * 1.03),
        ("Intervals", base_pace * 0.93),
    ]
    return [{"label": label, "value": _format_pace(value)} for label, value in zones]


def _actual_week_km(workouts: list[dict]) -> float:
    total = 0.0
    for workout in workouts:
        if str(workout.get("status") or "") not in {"completed", "modified"}:
            continue
        actual = _parse_patch_number(workout.get("actual_distance_km"))
        planned = _parse_patch_number(workout.get("distance_km"))
        total += actual if actual is not None else planned or 0.0
    return _round_half(total)


def _is_run_workout(workout: dict) -> bool:
    if str(workout.get("workout_type") or "").strip().lower() == "rest":
        return False
    distance = _parse_patch_number(workout.get("distance_km")) or 0.0
    return distance > 0


def _workout_status(workout: dict) -> str:
    return str(workout.get("status") or "planned").strip().lower()


def _workout_date_distance_key(workout: dict, run_date: date, run_distance: float | None) -> tuple[int, float, int]:
    scheduled = _coerce_date(workout.get("scheduled_date"))
    date_delta = abs((scheduled - run_date).days) if scheduled else 99
    planned_distance = _parse_patch_number(workout.get("distance_km")) or 0.0
    distance_delta = abs(planned_distance - run_distance) if run_distance is not None else 0.0
    day_index = int(workout.get("day_index") or 0)
    return (date_delta, distance_delta, day_index)


def _match_run_workout(
    uid: str,
    plan_id: str,
    week_id: str,
    *,
    requested_workout_id: str = "",
    run_date: date,
    run_distance: float | None,
    auto_match: bool = True,
) -> dict | None:
    workouts = _load_workouts(uid, plan_id, week_id)
    workout_by_id = {str(workout.get("id") or ""): workout for workout in workouts}
    requested = workout_by_id.get(str(requested_workout_id or ""))
    if requested and _is_run_workout(requested):
        return requested
    if not auto_match:
        return None

    runnable = [
        workout
        for workout in workouts
        if _is_run_workout(workout) and _workout_status(workout) not in {"completed", "modified", "skipped"}
    ]
    if not runnable:
        return None

    same_day = [workout for workout in runnable if _coerce_date(workout.get("scheduled_date")) == run_date]
    if same_day:
        return min(same_day, key=lambda item: _workout_date_distance_key(item, run_date, run_distance))

    return min(runnable, key=lambda item: _workout_date_distance_key(item, run_date, run_distance))


def _workout_completion_update(entry: dict, matched_workout: dict, now: datetime) -> tuple[dict, str]:
    run_distance = _parse_patch_number(entry.get("distance_km"))
    duration_seconds = entry.get("moving_time_seconds") or entry.get("duration_seconds")
    duration_min = int(round(duration_seconds / 60)) if duration_seconds else None
    planned_distance = _parse_patch_number((matched_workout or {}).get("distance_km"))
    status = "completed"
    if planned_distance is not None and run_distance is not None and abs(planned_distance - run_distance) >= 0.25:
        status = "modified"
    actual_text = f"{run_distance:g} km" if run_distance is not None else "the uploaded run"
    planned_text = f" Planned {planned_distance:g} km." if planned_distance is not None else ""
    return (
        {
            "status": status,
            "actual_distance_km": run_distance,
            "actual_duration_min": duration_min,
            "completion_effort": "",
            "completion_note": f"Logged {actual_text} from uploaded post-run screenshot.{planned_text} Map/location data ignored.",
            "progress_entry_id": entry.get("id"),
            "updated_at": now,
            "completed_at": now,
        },
        status,
    )


def _reconcile_todays_unmatched_run_entries(
    uid: str,
    plan_id: str,
    week_id: str,
    run_entries: list[dict],
) -> bool:
    today = date.today()
    changed = False
    for entry in run_entries:
        if entry.get("matched_workout_id"):
            continue
        if _coerce_date(entry.get("run_date")) != today:
            continue
        matched_workout = _match_run_workout(
            uid,
            plan_id,
            week_id,
            run_date=today,
            run_distance=_parse_patch_number(entry.get("distance_km")),
            auto_match=True,
        )
        matched_workout_id = str((matched_workout or {}).get("id") or "")
        entry_id = str(entry.get("id") or "")
        if not matched_workout_id or not entry_id:
            continue

        now = _now_utc()
        workout_update, status = _workout_completion_update(entry, matched_workout, now)
        batch = get_firestore_client().batch()
        batch.update(
            _plan_collection(uid).document(plan_id).collection("run_entries").document(entry_id),
            {
                "matched_week_id": week_id,
                "matched_workout_id": matched_workout_id,
                "updated_at": now,
            },
        )
        batch.update(_week_ref(uid, plan_id, week_id).collection("workouts").document(matched_workout_id), workout_update)
        batch.update(_week_ref(uid, plan_id, week_id), {"updated_at": now})
        batch.update(_plan_collection(uid).document(plan_id), {"updated_at": now})
        batch.commit()
        entry["matched_workout_id"] = matched_workout_id
        entry["matched_workout_status"] = status
        changed = True
        break
    return changed


def get_plan_dashboard(uid: str, profile: dict) -> dict:
    plan = ensure_active_plan(uid, profile)
    start_date_value = current_week_start()
    weeks = _load_weeks(uid, plan["id"], start_date_value=start_date_value, limit=PLAN_HORIZON_WEEKS)
    if not weeks:
        raise RuntimeError(f"Plan {plan['id']} has no generated weeks.")

    current_week = weeks[0]
    current_workouts = _load_workouts(uid, plan["id"], current_week["id"])
    readiness_entries = _load_readiness_entries(uid, plan["id"], limit=8)
    run_entries = _load_run_entries(uid, plan["id"], limit=8)
    if _reconcile_todays_unmatched_run_entries(uid, plan["id"], current_week["id"], run_entries):
        current_workouts = _load_workouts(uid, plan["id"], current_week["id"])
        run_entries = _load_run_entries(uid, plan["id"], limit=8)

    weekly_projection = [
        {
            "label": _format_week_range_label(week),
            "value": float(week.get("planned_km") or 0.0),
        }
        for week in weeks
    ]
    long_run_projection = []
    for week in weeks:
        workouts = _load_workouts(uid, plan["id"], week["id"])
        long_run = next((item for item in workouts if item.get("workout_type") == "long_run"), None)
        long_run_projection.append(
            {
                "label": _format_week_range_label(week),
                "value": float((long_run or {}).get("distance_km") or 0.0),
            }
        )

    workout_distribution_counter = Counter(workout.get("workout_type") or "easy" for workout in current_workouts)
    workout_distribution = [
        {"label": WORKOUT_TYPE_LABELS.get(workout_type, workout_type.title()), "value": count}
        for workout_type, count in sorted(workout_distribution_counter.items(), key=lambda item: item[0])
    ]
    fatigue_trend = []
    for entry in reversed(readiness_entries):
        logged_at = entry.get("created_at")
        stamp = logged_at.strftime("%b %d") if isinstance(logged_at, datetime) else "Recent"
        fatigue_trend.append({"label": stamp, "value": float(entry.get("overall_score") or 0.0)})

    current_week_km = float(current_week.get("planned_km") or 0.0)
    long_run = next((item for item in current_workouts if item.get("workout_type") == "long_run"), None)
    readiness_summary = _latest_readiness_summary(readiness_entries)
    goal_race_date = _goal_race_date_iso(profile) or _goal_race_date_iso(plan)

    return {
        "plan": plan,
        "weeks": weeks,
        "current_week": current_week,
        "current_week_id": current_week["id"],
        "current_workouts": current_workouts,
        "weekly_projection": weekly_projection,
        "long_run_projection": long_run_projection,
        "workout_distribution": workout_distribution,
        "fatigue_trend": fatigue_trend,
        "pace_zones": build_pace_zones(profile),
        "readiness_entries": readiness_entries,
        "readiness_summary": readiness_summary,
        "run_entries": run_entries,
        "summary": {
            "current_week_km": current_week_km,
            "actual_week_km": _actual_week_km(current_workouts),
            "completion_rate": _completion_rate(current_workouts),
            "long_run_km": float((long_run or {}).get("distance_km") or 0.0),
            "goal_distance": profile.get("goal_distance") or plan.get("goal_distance") or "Goal",
            "goal_race_date": goal_race_date,
            "week_focus": current_week.get("focus") or "Build consistency",
        },
    }


def build_plan_context(dashboard: dict) -> str:
    summary = dashboard.get("summary") or {}
    current_week = dashboard.get("current_week") or {}
    workouts = dashboard.get("current_workouts") or []
    readiness = dashboard.get("readiness_entries") or []
    run_entries = dashboard.get("run_entries") or []

    lines = [
        "ACTIVE PLAN SNAPSHOT:",
        f"- Goal distance: {summary.get('goal_distance') or 'Not set'}",
        f"- Goal race date: {summary.get('goal_race_date') or 'Not set'}",
        f"- Current week focus: {summary.get('week_focus') or 'Build consistency'}",
        f"- Planned KM this week: {summary.get('current_week_km') or 0}",
        f"- Current week note: {current_week.get('adjustment_note') or 'No manual adjustments yet.'}",
        "- Current workouts:",
    ]
    first_run = next(
        (
            workout
            for workout in sorted(workouts, key=lambda item: int(item.get("day_index") or 0))
            if str(workout.get("workout_type") or "").lower() != "rest"
            and float(workout.get("distance_km") or 0) > 0
        ),
        None,
    )
    if first_run:
        first_type = WORKOUT_TYPE_LABELS.get(first_run.get("workout_type"), first_run.get("workout_type"))
        first_detail = f"{first_run.get('day_name')}: {first_run.get('title')} ({first_type})"
        if str(first_run.get("workout_type") or "").lower() == "recovery":
            first_detail = f"{first_detail}. Note: the first run this week is already a recovery run."
        lines.append(f"- First run this week: {first_detail}")
    for workout in workouts:
        distance = workout.get("distance_km")
        duration = workout.get("duration_min")
        detail = f"{distance:g} km" if distance else ""
        if duration:
            detail = f"{detail} · {duration} min" if detail else f"{duration} min"
        actual = _parse_patch_number(workout.get("actual_distance_km"))
        if actual is not None and str(workout.get("status") or "").lower() in {"completed", "modified"}:
            detail = f"{detail} - actual={actual:g} km" if detail else f"actual={actual:g} km"
        lines.append(
            f"  - {workout.get('day_name')}: {workout.get('title')} ({WORKOUT_TYPE_LABELS.get(workout.get('workout_type'), workout.get('workout_type'))})"
            f"{' · ' + detail if detail else ''} · status={workout.get('status')}"
        )

    if readiness:
        latest = readiness[0]
        lines.append(
            "- Latest readiness:"
            f" sleep={latest.get('sleep')}/5,"
            f" soreness={latest.get('soreness')}/5,"
            f" energy={latest.get('energy')}/5,"
            f" motivation={latest.get('motivation')}/5,"
            f" pain_flag={bool(latest.get('pain_flag'))},"
            f" overall={latest.get('overall_score')}/5"
        )
    else:
        lines.append("- Latest readiness: none logged yet")
    if run_entries:
        latest_run = run_entries[0]
        lines.append(
            "- Latest uploaded run screenshot metrics:"
            f" date={latest_run.get('run_date') or 'unknown'},"
            f" distance_km={latest_run.get('distance_km')},"
            f" duration_seconds={latest_run.get('duration_seconds')},"
            f" average_pace_sec_per_km={latest_run.get('average_pace_sec_per_km')},"
            f" average_hr_bpm={latest_run.get('average_heart_rate_bpm')},"
            f" source_app={latest_run.get('source_app') or 'unknown'},"
            " map_data_ignored=True"
        )
    else:
        lines.append("- Uploaded run screenshot metrics: none yet")
    return "\n".join(lines)


def save_readiness_checkin(uid: str, plan_id: str, payload: dict) -> None:
    sleep = int(payload.get("sleep") or 1)
    soreness = int(payload.get("soreness") or 1)
    energy = int(payload.get("energy") or 1)
    motivation = int(payload.get("motivation") or 1)
    pain_flag = bool(payload.get("pain_flag"))
    overall = round(((sleep + energy + motivation + (6 - soreness)) / 4) - (0.4 if pain_flag else 0), 2)
    now = _now_utc()

    doc_payload = {
        "sleep": sleep,
        "soreness": soreness,
        "energy": energy,
        "motivation": motivation,
        "pain_flag": pain_flag,
        "notes": str(payload.get("notes") or "").strip(),
        "overall_score": max(1.0, min(5.0, overall)),
        "created_at": now,
        "updated_at": now,
    }
    ref = _plan_collection(uid).document(plan_id)
    ref.collection("readiness_entries").document().set(doc_payload)
    ref.update({"updated_at": now})


def update_workout_status(
    uid: str,
    plan_id: str,
    week_id: str,
    workout_id: str,
    *,
    status: str,
    effort: str = "",
    note: str = "",
) -> None:
    status_value = status if status in WORKOUT_STATUS_LABELS else "planned"
    effort_value = effort if effort in EFFORT_OPTIONS else ""
    now = _now_utc()
    _week_ref(uid, plan_id, week_id).collection("workouts").document(workout_id).update(
        {
            "status": status_value,
            "completion_effort": effort_value,
            "completion_note": note.strip(),
            "updated_at": now,
            "completed_at": now if status_value in {"completed", "modified"} else None,
        }
    )
    _week_ref(uid, plan_id, week_id).update({"updated_at": now})
    _plan_collection(uid).document(plan_id).update({"updated_at": now})


def save_run_progress_entry(
    uid: str,
    plan_id: str,
    week_id: str,
    payload: dict,
    *,
    workout_id: str = "",
    auto_match: bool = True,
) -> dict:
    now = _now_utc()
    entry_ref = _plan_collection(uid).document(plan_id).collection("run_entries").document()
    run_date = _coerce_date(payload.get("run_date")) or date.today()
    run_distance = _parse_patch_number(payload.get("distance_km"))
    matched_workout = _match_run_workout(
        uid,
        plan_id,
        week_id,
        requested_workout_id=workout_id,
        run_date=run_date,
        run_distance=run_distance,
        auto_match=auto_match,
    )
    matched_workout_id = str((matched_workout or {}).get("id") or "")
    entry = {
        "source": "screenshot_upload",
        "source_app": str(payload.get("source_app") or "").strip() or None,
        "run_date": run_date.isoformat(),
        "distance_km": run_distance,
        "duration_seconds": int(payload.get("duration_seconds") or 0) or None,
        "moving_time_seconds": int(payload.get("moving_time_seconds") or 0) or None,
        "average_pace_sec_per_km": int(payload.get("average_pace_sec_per_km") or 0) or None,
        "average_heart_rate_bpm": int(payload.get("average_heart_rate_bpm") or 0) or None,
        "max_heart_rate_bpm": int(payload.get("max_heart_rate_bpm") or 0) or None,
        "elevation_gain_m": _parse_patch_number(payload.get("elevation_gain_m")),
        "calories": int(payload.get("calories") or 0) or None,
        "splits": payload.get("splits") if isinstance(payload.get("splits"), list) else [],
        "confidence": _parse_patch_number(payload.get("confidence")),
        "summary": str(payload.get("summary") or "").strip()[:240],
        "missing_fields": payload.get("missing_fields") if isinstance(payload.get("missing_fields"), list) else [],
        "map_data_ignored": True,
        "image_stored": False,
        "matched_week_id": week_id,
        "matched_workout_id": matched_workout_id or None,
        "created_at": now,
        "updated_at": now,
    }
    batch = get_firestore_client().batch()
    batch.set(entry_ref, entry)

    matched_status = ""
    if matched_workout_id:
        entry["id"] = entry_ref.id
        workout_update, matched_status = _workout_completion_update(entry, matched_workout or {}, now)
        batch.update(_week_ref(uid, plan_id, week_id).collection("workouts").document(matched_workout_id), workout_update)

    batch.update(_week_ref(uid, plan_id, week_id), {"updated_at": now})
    batch.update(_plan_collection(uid).document(plan_id), {"updated_at": now})
    batch.commit()
    entry["id"] = entry_ref.id
    entry["matched_workout_status"] = matched_status or "unplanned"
    return entry


def _parse_patch_number(value) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isfinite(parsed):
        return parsed
    return None


def _recalculate_week_km(workouts: list[dict]) -> float:
    return _round_half(sum(float(item.get("distance_km") or 0.0) for item in workouts))


def apply_plan_patch(uid: str, plan_id: str, week_id: str, patch: dict) -> dict:
    week_ref = _week_ref(uid, plan_id, week_id)
    workouts = _load_workouts(uid, plan_id, week_id)
    workout_by_day = {str(item.get("day_name")): dict(item) for item in workouts}
    scale_pct = _parse_patch_number(patch.get("scale_week_pct")) or 0.0

    if scale_pct:
        scale = max(0.4, 1 + (scale_pct / 100.0))
        for workout in workout_by_day.values():
            distance = _parse_patch_number(workout.get("distance_km"))
            duration = _parse_patch_number(workout.get("duration_min"))
            if distance is not None:
                workout["distance_km"] = _round_half(max(0.0, distance * scale))
            if duration is not None:
                workout["duration_min"] = int(round(max(0.0, duration * scale)))
            workout["source"] = "assistant_apply"

    for item in patch.get("workouts") or []:
        day_name = str(item.get("day_name") or "").strip().title()
        if day_name not in DAY_INDEX:
            continue
        action = str(item.get("action") or "update").strip().lower()
        base = workout_by_day.get(day_name) or {
            "day_name": day_name,
            "day_index": DAY_INDEX[day_name],
            "scheduled_date": _day_date(_coerce_date(week_id) or current_week_start(), day_name).isoformat(),
            "status": "planned",
            "completion_effort": "",
            "completion_note": "",
        }
        updated = dict(base)
        updated["title"] = str(item.get("title") or updated.get("title") or "Plan update").strip()
        updated["workout_type"] = str(item.get("workout_type") or updated.get("workout_type") or "easy").strip().lower()
        updated["description"] = str(item.get("description") or updated.get("description") or "").strip()
        updated["effort_target"] = str(item.get("effort_target") or updated.get("effort_target") or "Moderate").strip().title()
        distance = _parse_patch_number(item.get("distance_km"))
        duration = _parse_patch_number(item.get("duration_min"))
        if distance is not None:
            updated["distance_km"] = _round_half(max(0.0, distance))
        if duration is not None:
            updated["duration_min"] = int(round(max(0.0, duration)))
        elif distance is not None:
            updated["duration_min"] = _minutes_for_distance(distance, workout_type=updated["workout_type"])
        updated["source"] = "assistant_apply"
        if action in {"replace", "update", "add"}:
            workout_by_day[day_name] = updated

    updated_workouts = sorted(workout_by_day.values(), key=lambda item: int(item.get("day_index", 0)))
    planned_km = _recalculate_week_km(updated_workouts)
    note_parts = [
        str(patch.get("summary") or "").strip(),
        str(patch.get("adjustment_note") or "").strip(),
    ]
    adjustment_note = " ".join(part for part in note_parts if part).strip()
    now = _now_utc()
    week_update = {
        "planned_km": planned_km,
        "adjustment_note": adjustment_note,
        "updated_at": now,
    }
    week_focus = str(patch.get("week_focus") or "").strip()
    if week_focus:
        week_update["focus"] = week_focus

    batch = get_firestore_client().batch()
    batch.update(week_ref, week_update)
    for workout in updated_workouts:
        workout_doc_id = str(workout.get("id") or f"{workout['day_name'].lower()}_{workout.get('workout_type', 'easy')}")
        workout["updated_at"] = now
        batch.set(week_ref.collection("workouts").document(workout_doc_id), workout, merge=True)
    batch.update(_plan_collection(uid).document(plan_id), {"updated_at": now})
    batch.commit()

    return {
        "planned_km": planned_km,
        "adjustment_note": adjustment_note,
        "workout_count": len(updated_workouts),
    }
