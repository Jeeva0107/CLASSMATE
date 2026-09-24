import re
from typing import Dict, Any

class ContextDetector:
    """
    Rule-Based NLP Context Detector for Classroom Audio Transcripts.
    Analyzes transcripts to identify classroom events and produce concise messages.
    """
    def __init__(self, student_name: str = "Jeeva"):
        self.student_name = student_name

    def set_student_name(self, name: str):
        """Update active student name to monitor for direct address."""
        if name and name.strip():
            self.student_name = name.strip()

    def analyze(self, transcript: str) -> Dict[str, Any]:
        """
        Analyze a transcript string and classify into event categories:
        - DIRECT_ADDRESS
        - QUESTION
        - ANNOUNCEMENT
        - INSTRUCTION
        - NORMAL_LECTURE
        """
        if not transcript or not transcript.strip() or transcript == "[No speech detected in audio]":
            return {
                "event_type": "NORMAL_LECTURE",
                "concise_message": "No active speech detected.",
                "original_transcript": transcript or "",
                "is_direct_address": False
            }

        text = transcript.strip()
        text_lower = text.lower()
        target_name_lower = self.student_name.lower()

        is_addressed = target_name_lower in text_lower

        announcement_keywords = [
            "assignment", "homework", "exam", "test", "quiz", "submit", "due",
            "submission", "deadline", "schedule", "cancelled", "postponed", "tomorrow",
            "next week", "grade", "marks", "announcement"
        ]

        instruction_keywords = [
            "open page", "turn to", "read", "write", "silence", "quiet",
            "look at", "take notes", "don't forget", "listen carefully", "start", "stop"
        ]

        question_starters = [
            "what", "why", "how", "when", "where", "who", "which",
            "can you", "could you", "do you", "are you", "is there", "have you"
        ]

        # Rule 1: Direct Address (Mentions student's name directly)
        if is_addressed:
            event_type = "DIRECT_ADDRESS"
            clean_msg = self._clean_addressed_message(text)
            return {
                "event_type": event_type,
                "concise_message": clean_msg,
                "original_transcript": text,
                "is_direct_address": True
            }

        # Rule 2: Question
        is_question = "?" in text or any(text_lower.startswith(q) for q in question_starters)
        if is_question:
            event_type = "QUESTION"
            return {
                "event_type": event_type,
                "concise_message": text,
                "original_transcript": text,
                "is_direct_address": False
            }

        # Rule 3: Announcement
        if any(kw in text_lower for kw in announcement_keywords):
            event_type = "ANNOUNCEMENT"
            return {
                "event_type": event_type,
                "concise_message": text,
                "original_transcript": text,
                "is_direct_address": False
            }

        # Rule 4: Instruction
        if any(kw in text_lower for kw in instruction_keywords):
            event_type = "INSTRUCTION"
            return {
                "event_type": event_type,
                "concise_message": text,
                "original_transcript": text,
                "is_direct_address": False
            }

        # Rule 5: Normal Lecture
        return {
            "event_type": "NORMAL_LECTURE",
            "concise_message": text,
            "original_transcript": text,
            "is_direct_address": False
        }

    def _clean_addressed_message(self, text: str) -> str:
        """Strip student name prefix if present to format concise message."""
        pattern = re.compile(rf'^{re.escape(self.student_name)}[\s,:-]*', re.IGNORECASE)
        cleaned = pattern.sub('', text).strip()
        if cleaned:
            # Capitalize first letter
            return cleaned[0].upper() + cleaned[1:]
        return text
