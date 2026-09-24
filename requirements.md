IMPORTANT: STOP ADDING FEATURES.

The current CLASSMATE UI looks polished but the CORE FUNCTIONALITY IS NOT WORKING.

The microphone is not actually recording audio and the application is currently more of a dashboard mockup than a working prototype.

We need to fix the CORE PIPELINE FIRST.

DO NOT ADD:
- Analytics
- Extra dashboards
- Hardware configuration pages
- Architecture page
- Complex settings
- Unnecessary navigation
- Decorative status indicators
- Fake system statuses
- Fake live events
- Extra features

Remove/hide these from the main interface for now.

==================================================
CORE FUNCTIONALITY REQUIRED
==================================================

The application must perform:

BROWSER MICROPHONE
        ↓
AUDIO RECORDING
        ↓
FASTER-WHISPER
        ↓
TRANSCRIPT
        ↓
CONTEXT DETECTION
        ↓
PRIORITY ENGINE
        ↓
STUDENT ALERT
        ↓
EVENT LOG

==================================================
1. MICROPHONE — MUST ACTUALLY WORK
==================================================

Use Streamlit's browser microphone/audio input functionality.

DO NOT attempt to access the laptop microphone directly using
PyAudio, sounddevice, or other local microphone libraries unless
absolutely necessary.

The browser should ask for microphone permission.

Create a simple interface:

[ 🎙 RECORD CLASSROOM AUDIO ]

The user should be able to record audio and stop recording.

After recording:

- Show the recorded audio player.
- Pass the recorded audio to Faster-Whisper.
- Show a loading indicator while transcription happens.
- Display the actual transcript.

If microphone permission is denied, show a clear error.

DO NOT show "SYSTEM: Listening" unless the microphone is actually
recording.

==================================================
2. SPEECH-TO-TEXT
==================================================

Use Faster-Whisper.

Default model:

Systran/faster-whisper-small

If this model is too slow or causes problems, allow fallback to:

Systran/faster-whisper-tiny

The model must ACTUALLY process the recorded audio.

Do not use predefined transcript text.

Test using:

"Jeeva, please submit your assignment tomorrow."

Expected output:

Jeeva, please submit your assignment tomorrow.

==================================================
3. CONTEXT DETECTION
==================================================

After transcription, automatically classify the transcript.

Supported events:

DIRECT_ADDRESS
QUESTION
ANNOUNCEMENT
INSTRUCTION
NORMAL_LECTURE

Example:

Transcript:
"Jeeva, please submit your assignment tomorrow."

Result:

Event:
DIRECT ADDRESS

Message:
"Please submit your assignment tomorrow."

==================================================
4. PRIORITY ENGINE
==================================================

Automatically assign:

P0 = Emergency
P1 = Directly relevant
P2 = Important
P3 = Normal

Examples:

Direct address → P1
Question to student → P1
Important announcement → P2
Assignment/deadline → P2
Normal lecture → P3

Show the result immediately after transcription.

==================================================
5. MAIN UI — SIMPLIFY IT
==================================================

The entire main page should focus on ONE workflow.

HEADER:

CLASSMATE
AI Classroom Accessibility Companion

SUBTITLE:

Turning classroom audio into meaningful accessible alerts.

Then:

------------------------------------------------

🎙 CLASSROOM AUDIO

[ RECORD AUDIO ]

OR

[ UPLOAD AUDIO ]

------------------------------------------------

📝 TRANSCRIPT

Show the actual Faster-Whisper transcript here.

------------------------------------------------

🧠 DETECTED EVENT

Event:
DIRECT ADDRESS

Message:
"Please submit your assignment tomorrow."

------------------------------------------------

🚦 PRIORITY

P1 — DIRECTLY RELEVANT

------------------------------------------------

📳 STUDENT ALERT

SPECIFIC HAPTIC ALERT

Display message:
"Assignment submission tomorrow."

------------------------------------------------

🕒 RECENT EVENTS

Show the latest 5 real processed events.

------------------------------------------------

IMPORTANT:

Do NOT display fake statuses such as:

"Speech STT: Ready"
"Context Detector: Ready"
"Priority Engine: Ready"

unless these are actually verified.

Do NOT display:

"Arduino: Not Connected"

on the main screen.

Do NOT make the main screen look like an engineering
configuration panel.

==================================================
6. DEMO MODE
==================================================

Keep Demo Mode, but make it secondary.

Add a small button:

[ Demo Mode ]

Demo Mode should contain:

1. Teacher addresses student
2. Question
3. Announcement
4. Class Bell
5. Emergency Alarm
6. Normal Lecture

Clearly label:

DEMO MODE — SIMULATED INPUT

Do not mix demo results with real microphone results.

==================================================
7. EVENT LOG
==================================================

Keep Event History because this is actually useful.

Every REAL processed event should be saved:

timestamp
transcript
event
message
priority
alert

Do not populate it with fake events on startup.

==================================================
8. ARDUINO
==================================================

DO NOT put Arduino configuration on the main dashboard.

Create only a small optional section:

HARDWARE OUTPUT
Arduino: Connected / Not Connected

If connected, send:

DIRECT_ADDRESS
QUESTION
ANNOUNCEMENT
BELL
EMERGENCY

to the Arduino through serial.

If not connected, the entire software must still work normally.

The software MUST NOT depend on Arduino.

==================================================
9. ERROR HANDLING
==================================================

Handle:

- Microphone permission denied
- No microphone available
- Empty recording
- Faster-Whisper model unavailable
- Unsupported audio format
- Transcription failure
- Arduino disconnected

Never display fake success states.

==================================================
10. TEST BEFORE FINISHING
==================================================

DO NOT tell me the application is complete until this works:

1. Open browser.
2. Click RECORD AUDIO.
3. Browser asks for microphone permission.
4. Speak:
   "Jeeva, please submit your assignment tomorrow."
5. Stop recording.
6. Audio is actually captured.
7. Faster-Whisper actually transcribes it.
8. Transcript appears.
9. Context detector identifies DIRECT_ADDRESS.
10. Priority engine assigns P1.
11. Student alert appears.
12. Event is saved to event history.

This exact workflow is the highest priority.

ONLY AFTER THIS WORKS should you improve the visual design.

The application should feel like a real AI accessibility product,
but FUNCTIONALITY is more important than decoration.