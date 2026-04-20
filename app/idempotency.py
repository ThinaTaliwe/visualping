import hashlib
from app.schemas import VisualpingEvent


def event_hash(event: VisualpingEvent) -> str:
    raw = f"{event.check_id}|{event.url}|{event.trigger_time.isoformat()}|{event.new_text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
