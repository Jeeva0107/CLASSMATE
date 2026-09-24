from typing import Dict, Any, List

class DemoRunner:
    """
    Demo Scenarios Engine for Hackathon Evaluators.
    Feeds simulated speech/audio through the exact SAME end-to-end processing pipeline:
    Context/Sound Classifier -> Priority Engine -> Alert -> Event Log -> Arduino Serial Output
    """
    SCENARIOS = {
        "1": {
            "title": "Teacher addresses student directly",
            "type": "speech",
            "raw_input": "Jeeva, can you answer this question?",
            "description": "Simulates teacher calling out the student's name directly in class."
        },
        "2": {
            "title": "Teacher asks a general question",
            "type": "speech",
            "raw_input": "What is supervised learning?",
            "description": "Simulates teacher posing a open question to the classroom."
        },
        "3": {
            "title": "Assignment deadline announcement",
            "type": "speech",
            "raw_input": "Your assignment must be submitted tomorrow.",
            "description": "Simulates critical assignment submission deadline announcement."
        },
        "4": {
            "title": "Exam schedule announcement",
            "type": "speech",
            "raw_input": "The mid-term exam will be conducted next Monday at 9 AM.",
            "description": "Simulates upcoming exam announcement."
        },
        "5": {
            "title": "Class period bell sound",
            "type": "sound",
            "sound_category": "CLASS_BELL",
            "raw_input": "[1800 Hz Ring Acoustic Tone]",
            "description": "Simulates period start/end bell sound in hallway."
        },
        "6": {
            "title": "Emergency fire alarm sound",
            "type": "sound",
            "sound_category": "EMERGENCY_ALARM",
            "raw_input": "[Continuous High-Decibel Siren]",
            "description": "Simulates urgent emergency fire alarm sound."
        },
        "7": {
            "title": "Normal continuous lecture background",
            "type": "speech",
            "raw_input": "Supervised learning algorithms use labeled datasets to train predictive machine learning models...",
            "description": "Simulates ongoing standard lecture content."
        }
    }

    def __init__(self, context_detector, sound_classifier, priority_engine, arduino_controller, event_logger):
        self.context_detector = context_detector
        self.sound_classifier = sound_classifier
        self.priority_engine = priority_engine
        self.arduino_controller = arduino_controller
        self.event_logger = event_logger

    def get_scenarios_list(self) -> List[Dict[str, Any]]:
        """Return formatted list of scenario choices for Streamlit UI."""
        return [
            {"id": key, "title": val["title"], "type": val["type"], "description": val["description"]}
            for key, val in self.SCENARIOS.items()
        ]

    def run_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """
        Execute specified scenario through the complete live processing pipeline.
        """
        scenario = self.SCENARIOS.get(str(scenario_id))
        if not scenario:
            raise ValueError(f"Invalid Scenario ID: {scenario_id}")

        if scenario["type"] == "speech":
            raw_text = scenario["raw_input"]
            # 1. Pipeline Step 1: Context Detection
            context_res = self.context_detector.analyze(raw_text)
            context_res["source"] = "demo_speech"

            # 2. Pipeline Step 2: Priority Engine
            priority_res = self.priority_engine.process_event(context_res)

        else:  # sound scenario
            sound_cat = scenario["sound_category"]
            # 1. Pipeline Step 1: Sound Classifier
            sound_res = self.sound_classifier.simulate_sound_event(sound_cat)
            sound_res["source"] = "demo_sound"

            # 2. Pipeline Step 2: Priority Engine
            priority_res = self.priority_engine.process_event(sound_res)
            raw_text = sound_res["concise_message"]

        # Mark explicitly as DEMO MODE output
        priority_res["is_demo"] = True

        # 3. Pipeline Step 3: Event Logging
        logged_record = self.event_logger.log_event(priority_res)

        # 4. Pipeline Step 4: Arduino Output Trigger
        self.arduino_controller.send_event_command(priority_res)

        return {
            "scenario": scenario,
            "raw_input": raw_text,
            "pipeline_output": priority_res,
            "log_record": logged_record,
            "arduino_command": self.arduino_controller.last_sent_command
        }
