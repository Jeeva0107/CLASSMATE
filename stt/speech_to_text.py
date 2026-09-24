import os
import tempfile
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("classmate.stt")

class AudioTranscriber:
    """
    Speech-To-Text wrapper powered by Faster-Whisper.
    Transcribes browser recorded audio (st.audio_input) or uploaded audio files.
    """
    def __init__(self, model_size: str = "tiny", device: str = "cpu", compute_type: str = "int8"):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None
        self._is_loaded = False
        self.last_error = None

    def load_model(self) -> bool:
        """Lazy loader for Faster-Whisper model."""
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
            logger.warning(f"Failed to load Faster-Whisper model ({self.model_size}): {e}")
            self._is_loaded = False
            return False

    def is_ready(self) -> bool:
        """Check if model is loaded or available."""
        return self.load_model()

    def transcribe_file(self, file_bytes_or_path, language: str = "en") -> Dict[str, Any]:
        """
        Transcribe audio file bytes (from st.audio_input / st.file_uploader) or path using Faster-Whisper.
        """
        if not self.load_model() or self.model is None:
            return {
                "status": "error",
                "transcript": "",
                "error": f"Faster-Whisper model failed to load: {self.last_error}",
                "engine": "Faster-Whisper (Failed)"
            }

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
            logger.error(f"Transcription error: {e}")
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            return {
                "status": "error",
                "transcript": "",
                "error": f"Audio processing error: {str(e)}",
                "engine": "Faster-Whisper (Error)"
            }
