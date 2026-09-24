from typing import Dict, Any

class SoundClassifier:
    """
    Environmental Audio Classifier for non-speech classroom events.
    Analyzes audio pitch/frequency features or demo triggers to detect:
    - CLASS_BELL
    - EMERGENCY_ALARM
    - OTHER_SOUND
    """
    def __init__(self):
        self.is_ready = True

    def classify_audio_buffer(self, audio_data, sample_rate: int = 16000) -> Dict[str, Any]:
        """
        Classify raw audio buffer using spectral peak/energy heuristics.
        """
        if audio_data is None:
            return {
                "event_type": "OTHER_SOUND",
                "confidence": 0.0,
                "concise_message": "Ambient room audio",
                "is_demo": False
            }

        try:
            # pyrefly: ignore [missing-import]
            import numpy as np
            if len(audio_data) == 0:
                return {
                    "event_type": "OTHER_SOUND",
                    "confidence": 0.0,
                    "concise_message": "Ambient room audio",
                    "is_demo": False
                }

            fft_vals = np.abs(np.fft.rfft(audio_data))
            freqs = np.fft.rfftfreq(len(audio_data), 1.0 / sample_rate)

            max_freq_idx = np.argmax(fft_vals)
            peak_freq = freqs[max_freq_idx]
            energy = np.mean(audio_data ** 2)

            if 1200 <= peak_freq <= 3500 and energy > 0.02:
                return {
                    "event_type": "CLASS_BELL",
                    "confidence": 0.88,
                    "concise_message": f"Class Bell Ring Detected ({int(peak_freq)} Hz)",
                    "is_demo": False
                }
            elif 700 <= peak_freq <= 1200 and energy > 0.05:
                return {
                    "event_type": "EMERGENCY_ALARM",
                    "confidence": 0.94,
                    "concise_message": "Emergency Siren Alarm Detected",
                    "is_demo": False
                }
            else:
                return {
                    "event_type": "OTHER_SOUND",
                    "confidence": 0.50,
                    "concise_message": "Background Classroom Audio",
                    "is_demo": False
                }
        except Exception as e:
            return {
                "event_type": "OTHER_SOUND",
                "confidence": 0.5,
                "concise_message": "Environmental Ambient Sound",
                "is_demo": False
            }

    def simulate_sound_event(self, sound_category: str) -> Dict[str, Any]:
        """
        Trigger a clear DEMO MODE environmental sound classification.
        """
        if sound_category == "CLASS_BELL":
            return {
                "event_type": "CLASS_BELL",
                "confidence": 0.98,
                "concise_message": "Class Bell Detected [DEMO MODE]",
                "is_demo": True
            }
        elif sound_category == "EMERGENCY_ALARM":
            return {
                "event_type": "EMERGENCY_ALARM",
                "confidence": 0.99,
                "concise_message": "Emergency Alarm Signal Detected [DEMO MODE]",
                "is_demo": True
            }
        else:
            return {
                "event_type": "OTHER_SOUND",
                "confidence": 0.70,
                "concise_message": "Environmental Ambient Sound [DEMO MODE]",
                "is_demo": True
            }
