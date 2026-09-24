from typing import Dict, Any

class PriorityEngine:
    """
    Rule-Based Priority Engine for CLASSMATE.
    Maps detected events & non-speech sounds into clear priority levels & alert patterns.
    """

    PRIORITY_MAPPINGS = {
        # Environmental sounds & Emergencies
        "EMERGENCY_ALARM": {
            "priority": "P0",
            "priority_label": "Emergency",
            "alert_type": "STRONG_ALERT",
            "haptic_pattern": "Continuous Strong Vibration + Rapid Blink"
        },
        "CLASS_BELL": {
            "priority": "P1",
            "priority_label": "Directly Relevant",
            "alert_type": "SPECIFIC_ALERT",
            "haptic_pattern": "Double Pulses + Pulse Blink"
        },
        # Speech Events
        "DIRECT_ADDRESS": {
            "priority": "P1",
            "priority_label": "Directly Relevant",
            "alert_type": "SPECIFIC_ALERT",
            "haptic_pattern": "Distinct Double Vibration + Double Flash"
        },
        "QUESTION": {
            "priority": "P1",
            "priority_label": "Directly Relevant",
            "alert_type": "SPECIFIC_ALERT",
            "haptic_pattern": "Single Long Vibration + Soft Pulse"
        },
        "ANNOUNCEMENT": {
            "priority": "P2",
            "priority_label": "Important",
            "alert_type": "SHORT_ALERT",
            "haptic_pattern": "Single Short Tap + Short Blink"
        },
        "INSTRUCTION": {
            "priority": "P2",
            "priority_label": "Important",
            "alert_type": "SHORT_ALERT",
            "haptic_pattern": "Single Short Tap"
        },
        "NORMAL_LECTURE": {
            "priority": "P3",
            "priority_label": "Normal / Background",
            "alert_type": "NO_DISRUPTIVE_ALERT",
            "haptic_pattern": "Silent / Visual Only"
        },
        "OTHER_SOUND": {
            "priority": "P3",
            "priority_label": "Normal / Background",
            "alert_type": "NO_DISRUPTIVE_ALERT",
            "haptic_pattern": "Silent"
        }
    }

    def process_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input event dictionary containing event_type and concise_message.
        Returns complete priority decision dict.
        """
        event_type = event_data.get("event_type", "NORMAL_LECTURE")
        concise_msg = event_data.get("concise_message", "")

        # Check for emergency keywords in speech even if context classified as instruction/announcement
        transcript_lower = str(event_data.get("original_transcript", "")).lower()
        if any(term in transcript_lower for term in ["fire", "evacuate", "emergency", "lockdown"]):
            event_type = "EMERGENCY_ALARM"

        mapping = self.PRIORITY_MAPPINGS.get(event_type, self.PRIORITY_MAPPINGS["NORMAL_LECTURE"])

        return {
            "priority": mapping["priority"],
            "priority_label": mapping["priority_label"],
            "alert_type": mapping["alert_type"],
            "event_type": event_type,
            "concise_message": concise_msg if concise_msg else "Classroom Event Detected",
            "haptic_pattern": mapping["haptic_pattern"],
            "source": event_data.get("source", "speech")
        }
