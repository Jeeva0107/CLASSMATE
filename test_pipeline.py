import sys
import os

from stt.speech_to_text import AudioTranscriber
from context.context_detector import ContextDetector
from priority.priority_engine import PriorityEngine
from sound_classifier.sound_classifier import SoundClassifier
from hardware.arduino_controller import ArduinoController
from event_log.event_logger import EventLogger
from demo.demo_scenarios import DemoRunner

def test_full_pipeline():
    print("==================================================")
    print("Testing CLASSMATE Processing Pipeline...")
    print("==================================================")

    # 1. Initialize modules
    stt = AudioTranscriber()
    context = ContextDetector(student_name="Jeeva")
    priority = PriorityEngine()
    sound = SoundClassifier()
    arduino = ArduinoController()
    logger = EventLogger(data_filepath="data/test_events.json")

    demo = DemoRunner(context, sound, priority, arduino, logger)

    # Test Speech Pipeline
    test_cases = [
        ("Jeeva, can you answer this question?", "DIRECT_ADDRESS", "P1"),
        ("What is supervised learning?", "QUESTION", "P1"),
        ("Your assignment must be submitted tomorrow.", "ANNOUNCEMENT", "P2"),
        ("Open page 42 and read the first paragraph.", "INSTRUCTION", "P2"),
        ("Supervised learning uses labeled data.", "NORMAL_LECTURE", "P3"),
        ("Attention! Fire emergency! Evacuate immediately!", "EMERGENCY_ALARM", "P0")
    ]

    print("\n--- Speech Context & Priority Tests ---")
    for transcript, expected_event, expected_prio in test_cases:
        ctx_res = context.analyze(transcript)
        prio_res = priority.process_event(ctx_res)
        logged = logger.log_event(prio_res)

        print(f"Input: '{transcript}'")
        print(f" -> Event: {prio_res['event_type']} (Expected: {expected_event})")
        print(f" -> Priority: {prio_res['priority']} (Expected: {expected_prio})")
        print(f" -> Alert: {prio_res['alert_type']}")
        print(f" -> Logged: {logged['timestamp']} | {logged['message']}\n")

        assert prio_res['event_type'] == expected_event, f"Mismatch event: {prio_res['event_type']} vs {expected_event}"
        assert prio_res['priority'] == expected_prio, f"Mismatch priority: {prio_res['priority']} vs {expected_prio}"

    print("--- Sound Classifier Demo Tests ---")
    sound_res = sound.simulate_sound_event("CLASS_BELL")
    prio_sound = priority.process_event(sound_res)
    print(f"Class Bell -> Event: {prio_sound['event_type']}, Priority: {prio_sound['priority']}")
    assert prio_sound['event_type'] == "CLASS_BELL" and prio_sound['priority'] == "P1"

    print("\n--- Demo Scenarios Engine Test ---")
    sc_res = demo.run_scenario("1")
    print(f"Scenario 1 Output: Event={sc_res['pipeline_output']['event_type']}, Priority={sc_res['pipeline_output']['priority']}")

    # Clean up test json
    if os.path.exists("data/test_events.json"):
        os.remove("data/test_events.json")

    print("\n[SUCCESS] ALL PIPELINE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_full_pipeline()
