# CLASSMATE – AI-Powered Classroom Accessibility Companion

CLASSMATE is an AI-powered classroom accessibility companion for deaf and hard-of-hearing students. It listens to classroom audio, transcribes live speech, detects non-speech environmental sound events, classifies context, applies a priority engine, and provides real-time haptic/visual alerts alongside physical Arduino hardware feedback.

---

## 📌 Problem Statement

Deaf and hard-of-hearing students face significant accessibility hurdles in conventional classroom environments:
1. **Missed Direct Addresses:** Hearing when a teacher calls out their name or asks a question directly.
2. **Environmental Sound Isolation:** Missing acoustic cues like class period bells or emergency alarms.
3. **Information Overload:** Difficulty distinguishing crucial announcements (e.g. deadline changes) from continuous background lecture text.

---

## 💡 Solution

CLASSMATE acts as an intelligent accessibility layer between classroom acoustic environments and deaf students:
- **Speech-to-Text (STT):** Real-time transcription using Faster-Whisper.
- **Context Detection:** Rule-based NLP classifier categorizing speech into `DIRECT_ADDRESS`, `QUESTION`, `ANNOUNCEMENT`, `INSTRUCTION`, or `NORMAL_LECTURE`.
- **Environmental Sound Classification:** Non-speech acoustic classifier for `CLASS_BELL` and `EMERGENCY_ALARM`.
- **Priority Engine:** Intelligent mapping into priority levels (`P0` Emergency, `P1` Directly Relevant, `P2` Important, `P3` Normal) and custom alert modes (`STRONG_ALERT`, `SPECIFIC_ALERT`, `SHORT_ALERT`, `NO_DISRUPTIVE_ALERT`).
- **Arduino Hardware Integration:** Serial output protocol driving physical LCD screen & LED indicator alerts on an Arduino Uno prototype.
- **Repeat Last Message:** Dedicated instant recap feature for the student's physical wearable interface.

---

## 🏗️ System Architecture

```
                      +---------------------------------------------------+
                      |            CLASSROOM ENVIRONMENT INPUT            |
                      +-------------------------+-------------------------+
                                                |
                   +----------------------------+----------------------------+
                   |                                                         |
                   v                                                         v
         [ Classroom Audio ]                                       [ Environmental Audio ]
                   |                                                         |
                   v                                                         v
        +--------------------+                                    +--------------------+
        |   Speech-to-Text   |                                    | Sound Classifier   |
        |  (Faster-Whisper)  |                                    | (Class Bell/Alarm) |
        +----------+---------+                                    +----------+---------+
                   |                                                         |
                   v                                                         |
        +--------------------+                                               |
        | Context Detector   |                                               |
        | (NLP Rules/LLM)    |                                               |
        +----------+---------+                                               |
                   |                                                         |
                   +----------------------------+----------------------------+
                                                |
                                                v
                                     +---------------------+
                                     |   PRIORITY ENGINE   |
                                     |   (P0, P1, P2, P3)  |
                                     +----------+----------+
                                                |
                                                v
                                     +---------------------+
                                     |    STUDENT ALERT    |
                                     |   & EVENT LOGGER    |
                                     +----------+----------+
                                                |
                                                v
                               +---------------------------------+
                               |     CURRENT PROTOTYPE OUTPUT    |
                               |       Arduino Uno Controller    |
                               |        (LCD Display + LED)      |
                               +---------------------------------+
```

---

## 🛠️ Technology Stack

- **Python 3.9+**
- **Streamlit** (Web Dashboard UI)
- **Faster-Whisper** (Speech Recognition Engine)
- **NumPy & SciPy** (Acoustic signal analysis)
- **PySerial** (Hardware communication with Arduino)
- **Pandas** (Event history logging)

---

## 🚀 Quickstart & Installation Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🔌 Connecting Arduino Hardware

1. Upload the provided C++ sketch (`hardware/arduino_sketch.ino`) to your Arduino Uno via Arduino IDE.
2. Wire the LCD (16x2) to pins 12, 11, 5, 4, 3, 2 and LED indicator to Pin 13.
3. Connect the Arduino via USB to your computer.
4. Open the CLASSMATE dashboard sidebar, select your COM port, and click **Connect Serial Hardware**.

> *Note: CLASSMATE works completely standalone in offline mode even if Arduino is disconnected.*

---

## 🧪 Demo Mode (Evaluator Guide)

Navigate to the **Demo Mode (Evaluator)** tab in the dashboard to test 7 pre-configured scenarios:
1. **Teacher addresses student directly** (`DIRECT_ADDRESS` -> P1)
2. **Teacher asks a question** (`QUESTION` -> P1)
3. **Assignment announcement** (`ANNOUNCEMENT` -> P2)
4. **Exam announcement** (`ANNOUNCEMENT` -> P2)
5. **Class period bell sound** (`CLASS_BELL` -> P1)
6. **Emergency fire alarm sound** (`EMERGENCY_ALARM` -> P0)
7. **Normal continuous lecture** (`NORMAL_LECTURE` -> P3)

Each scenario feeds through the **exact same processing pipeline** and updates the live dashboard, event logger, and Arduino serial hardware!

---

## 🔮 Future Roadmap & Hardware Integration

- **Embedded Wearable:** Replace Arduino Uno prototype with a compact ESP32 / BLE wristband featuring discrete ERM/LRA vibration motors.
- **LLM Context Refinement:** Integrate fine-tuned local LLM (e.g. Llama-3-8B-Instruct) for complex multi-speaker classroom reasoning.
- **Directional Microphones:** Multi-channel spatial audio array to indicate teacher position in the classroom.
