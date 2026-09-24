import os
import tempfile
import logging
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger("classmate.stt")

class AudioTranscriber:
    """
    Speech-To-Text engine supporting:
    1. Local Faster-Whisper model execution (when available locally)
    2. Remote API boundary via STT_API_URL / OPENAI_API_KEY (for cloud serverless deployments)
    """
    def __init__(self, model_size: str = "tiny", device: str = "cpu", compute_type: str = "int8", api_url: Optional[str] = None):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.api_url = api_url or os.getenv("STT_API_URL")
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("STT_API_KEY")
        self.model = None
        self._is_loaded = False
        self.last_error = None

    def load_model(self) -> bool:
        """Lazy loader for local Faster-Whisper model."""
        if self._is_loaded and self.model is not None:
            return True
        try:
            from faster_whisper import WhisperModel
            logger.info(f"Loading Faster-Whisper model ({self.model_size})...")
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )
            self._is_loaded = True
            self.last_error = None
            return True
        except Exception as e:
            self.last_error = str(e)
            logger.warning(f"Local Faster-Whisper unavailable: {e}")
            self._is_loaded = False
            return False

    def is_ready(self) -> bool:
        """Check if local model or remote API endpoint is ready."""
        return self.load_model() or bool(self.api_url or self.api_key)

    def transcribe_file(self, file_bytes_or_path, language: str = "en") -> Dict[str, Any]:
        """
        Transcribe audio file bytes or path using local Faster-Whisper, or remote API endpoint fallback.
        """
        # 1. Try local Faster-Whisper first
        if self.load_model() and self.model is not None:
            temp_path = None
            try:
                if isinstance(file_bytes_or_path, (bytes, bytearray)):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        tmp.write(file_bytes_or_path)
                        temp_path = tmp.name
                    target_file = temp_path
                else:
                    target_file = file_bytes_or_path

                segments, info = self.model.transcribe(
                    target_file,
                    beam_size=5,
                    language=language,
                    vad_filter=True
                )

                transcript_text = " ".join([segment.text.strip() for segment in segments]).strip()

                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass

                return {
                    "status": "success",
                    "transcript": transcript_text if transcript_text else "[No speech detected in audio]",
                    "language": getattr(info, "language", language),
                    "confidence": getattr(info, "language_probability", 1.0),
                    "engine": f"Faster-Whisper ({self.model_size})"
                }
            except Exception as e:
                logger.error(f"Local Faster-Whisper transcription error: {e}")
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass

        # 2. Remote API boundary fallback (for cloud serverless deployments)
        if self.api_url or self.api_key:
            try:
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"

                if isinstance(file_bytes_or_path, (bytes, bytearray)):
                    audio_data = file_bytes_or_path
                else:
                    with open(file_bytes_or_path, "rb") as f:
                        audio_data = f.read()

                files = {"file": ("audio.wav", audio_data, "audio/wav")}
                data = {"model": "whisper-1", "language": language}
                target_url = self.api_url or "https://api.openai.com/v1/audio/transcriptions"

                response = requests.post(target_url, headers=headers, files=files, data=data, timeout=30)
                if response.status_code == 200:
                    res_json = response.json()
                    transcript_text = res_json.get("text", "").strip()
                    return {
                        "status": "success",
                        "transcript": transcript_text if transcript_text else "[No speech detected]",
                        "language": language,
                        "confidence": 0.95,
                        "engine": "Remote Whisper API"
                    }
                else:
                    return {
                        "status": "error",
                        "transcript": "",
                        "error": f"Remote API Error ({response.status_code}): {response.text}",
                        "engine": "Remote Whisper API (Error)"
                    }
            except Exception as e:
                return {
                    "status": "error",
                    "transcript": "",
                    "error": f"Remote STT connection error: {str(e)}",
                    "engine": "Remote Whisper API (Error)"
                }

        return {
            "status": "error",
            "transcript": "",
            "error": f"Faster-Whisper model not available locally and STT_API_URL not configured: {self.last_error}",
            "engine": "STT Engine (Unavailable)"
        }
