import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class EventLogger:
    """
    JSON File Event Storage for CLASSMATE.
    Logs each processed classroom event and manages history for dashboard display.
    """
    def __init__(self, data_filepath: str = "data/events.json"):
        self.data_filepath = data_filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create data directory and events file if missing."""
        dir_name = os.path.dirname(self.data_filepath)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        if not os.path.exists(self.data_filepath):
            with open(self.data_filepath, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    def log_event(self, priority_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record a new event to JSON file and return complete logged record.
        """
        now = datetime.now()
        record = {
            "timestamp": now.strftime("%H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "event": priority_data.get("event_type", "NORMAL_LECTURE"),
            "message": priority_data.get("concise_message", ""),
            "priority": priority_data.get("priority", "P3"),
            "alert": priority_data.get("alert_type", "NO_DISRUPTIVE_ALERT"),
            "source": priority_data.get("source", "speech")
        }

        events = self.get_all_events()
        events.insert(0, record)  # Newest first

        try:
            with open(self.data_filepath, "w", encoding="utf-8") as f:
                json.dump(events, f, indent=2)
        except Exception as e:
            print(f"Error saving event log: {e}")

        return record

    def get_all_events(self) -> List[Dict[str, Any]]:
        """Retrieve all logged events."""
        if not os.path.exists(self.data_filepath):
            return []
        try:
            with open(self.data_filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def get_recent_events(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get top N recent events."""
        return self.get_all_events()[:limit]

    def get_last_important_event(self) -> Optional[Dict[str, Any]]:
        """Get the most recent event with priority P0, P1, or P2."""
        events = self.get_all_events()
        for evt in events:
            if evt.get("priority") in ["P0", "P1", "P2"]:
                return evt
        return events[0] if events else None

    def clear_events(self):
        """Clear all event history."""
        try:
            with open(self.data_filepath, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
        except Exception as e:
            print(f"Error clearing event log: {e}")
