import os
import sys
from http.server import BaseHTTPRequestHandler

# Vercel Serverless Function entrypoint exports
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>CLASSMATE AI Classroom Companion</h1>")
        return

app = handler
application = handler

# Ensure project root is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stt.speech_to_text import AudioTranscriber
from context.context_detector import ContextDetector
from priority.priority_engine import PriorityEngine
from sound_classifier.sound_classifier import SoundClassifier
from hardware.arduino_controller import ArduinoController
from event_log.event_logger import EventLogger
from demo.demo_scenarios import DemoRunner
import streamlit as st

# Page Config
st.set_page_config(
    page_title="CLASSMATE — AI Classroom Accessibility Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Refined Dark Theme & Professional Product Styling (Linear / Notion Aesthetic)
st.markdown("""
<style>
    /* Hide Streamlit Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Global Base */
    .stApp {
        background-color: #090d16;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* Layout Container Constraints */
    .main .block-container {
        max-width: 1040px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    /* Top Application Shell Header */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 24px;
        margin-bottom: 28px;
        background: linear-gradient(180deg, #131822 0%, #0d1117 100%);
        border: 1px solid #212836;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .brand-container {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .brand-logo-box {
        width: 46px;
        height: 46px;
        border-radius: 12px;
        background: linear-gradient(135deg, #1f6beb 0%, #0d419d 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 4px 14px rgba(31, 107, 235, 0.35);
        flex-shrink: 0;
    }
    .brand-logo-box svg {
        width: 24px;
        height: 24px;
        fill: #ffffff;
    }
    .brand-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(180deg, #ffffff 0%, #d0d7de 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 12px;
        line-height: 1.1;
    }
    .brand-tag {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 12px;
        background: rgba(56, 139, 253, 0.15);
        color: #58a6ff;
        border: 1px solid rgba(56, 139, 253, 0.3);
        -webkit-text-fill-color: #58a6ff;
        line-height: 1;
    }
    .brand-subtitle {
        font-size: 0.92rem;
        color: #8b949e;
        margin-top: 4px;
        font-weight: 400;
        letter-spacing: -0.01em;
    }
    .header-status-group {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.78rem;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 20px;
        background-color: rgba(46, 160, 67, 0.12);
        color: #3fb950;
        border: 1px solid rgba(46, 160, 67, 0.3);
    }
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #3fb950;
    }
    .status-badge-offline {
        background-color: rgba(139, 148, 158, 0.1);
        color: #8b949e;
        border: 1px solid rgba(139, 148, 158, 0.2);
    }
    .status-dot-offline {
        background-color: #8b949e;
    }

    /* Section Cards */
    .panel-card {
        background-color: #131822;
        border: 1px solid #212836;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }
    .panel-title {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #8b949e;
        margin-bottom: 6px;
    }
    .panel-description {
        font-size: 0.85rem;
        color: #8b949e;
        margin-bottom: 16px;
    }

    /* Transcript Box */
    .transcript-box {
        background-color: #0d1117;
        border: 1px solid #212836;
        border-radius: 8px;
        padding: 18px 20px;
        font-size: 1.15rem;
        line-height: 1.6;
        color: #f0f6fc;
        min-height: 70px;
        display: flex;
        align-items: center;
    }
    .transcript-placeholder {
        color: #6e7681;
        font-style: italic;
        font-size: 0.95rem;
    }

    /* Priority Badges */
    .priority-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.03em;
    }
    .badge-P0 {
        background-color: #3d1618;
        color: #ff7b72;
        border: 1px solid #f85149;
    }
    .badge-P1 {
        background-color: #342507;
        color: #f0883e;
        border: 1px solid #d29922;
    }
    .badge-P2 {
        background-color: #132c44;
        color: #58a6ff;
        border: 1px solid #388bfd;
    }
    .badge-P3 {
        background-color: #161b22;
        color: #8b949e;
        border: 1px solid #30363d;
    }

    /* Intelligence Display */
    .intel-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f0f6fc;
        margin-bottom: 4px;
    }
    .intel-desc {
        font-size: 0.88rem;
        color: #8b949e;
    }

    /* Accessibility Alert Panel (Focal Point) */
    .alert-hero-card {
        background: linear-gradient(180deg, #161f2e 0%, #101622 100%);
        border: 1px solid #2f81f7;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .alert-hero-card.p0-alert {
        border-color: #f85149;
        background: linear-gradient(180deg, #2a1518 0%, #150d0f 100%);
    }
    .alert-hero-card.p1-alert {
        border-color: #d29922;
        background: linear-gradient(180deg, #241c10 0%, #141009 100%);
    }
    .alert-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #58a6ff;
        margin-bottom: 8px;
    }
    .alert-headline {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f0f6fc;
        margin-bottom: 8px;
    }
    .alert-message {
        font-size: 1.05rem;
        color: #d0d7de;
        margin-bottom: 16px;
    }
    .alert-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-top: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    .alert-haptic-info {
        font-size: 0.8rem;
        color: #8b949e;
    }

    /* History Table Styling */
    .history-row {
        display: grid;
        grid-template-columns: 80px 140px 60px 1fr;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        border-bottom: 1px solid #1c2128;
        font-size: 0.85rem;
    }
    .history-header {
        font-weight: 600;
        color: #8b949e;
        border-bottom: 1px solid #30363d;
        padding-bottom: 8px;
    }
    .history-time {
        color: #6e7681;
        font-family: monospace;
    }
    .history-event {
        color: #c9d1d9;
        font-weight: 500;
    }

    /* Custom Streamlit Tabs & Buttons */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #212836;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        padding: 0 16px;
        background-color: transparent;
        border-radius: 6px 6px 0 0;
        color: #8b949e;
        font-size: 0.85rem;
        font-weight: 500;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1c2128 !important;
        color: #f0f6fc !important;
        border-bottom: 2px solid #2f81f7 !important;
    }
    button[kind="secondary"], button[kind="primary"] {
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Core Services in Session State
if "stt_engine" not in st.session_state:
    st.session_state.stt_engine = AudioTranscriber(model_size="tiny")

if "context_detector" not in st.session_state:
    st.session_state.context_detector = ContextDetector(student_name="Jeeva")

if "priority_engine" not in st.session_state:
    st.session_state.priority_engine = PriorityEngine()

if "sound_classifier" not in st.session_state:
    st.session_state.sound_classifier = SoundClassifier()

if "arduino_controller" not in st.session_state:
    st.session_state.arduino_controller = ArduinoController()

if "event_logger" not in st.session_state:
    st.session_state.event_logger = EventLogger()

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "processed_audio_id" not in st.session_state:
    st.session_state.processed_audio_id = None

demo_runner = DemoRunner(
    context_detector=st.session_state.context_detector,
    sound_classifier=st.session_state.sound_classifier,
    priority_engine=st.session_state.priority_engine,
    arduino_controller=st.session_state.arduino_controller,
    event_logger=st.session_state.event_logger
)

# Pipeline Processing Function
def process_audio_bytes(audio_bytes: bytes, source_name: str = "microphone"):
    with st.spinner("Processing classroom audio..."):
        stt_result = st.session_state.stt_engine.transcribe_file(audio_bytes)
        
        if stt_result["status"] == "error":
            st.error(f"Audio Processing Error: {stt_result.get('error')}")
            return None

        transcript = stt_result["transcript"]
        context_res = st.session_state.context_detector.analyze(transcript)
        context_res["source"] = source_name

        priority_res = st.session_state.priority_engine.process_event(context_res)
        priority_res["original_transcript"] = transcript
        priority_res["is_demo"] = False

        # Log event & send hardware serial command
        st.session_state.event_logger.log_event(priority_res)
        st.session_state.arduino_controller.send_event_command(priority_res)

        st.session_state.current_result = priority_res
        return priority_res


# --------------------------------------------------
# TOP APPLICATION HEADER SHELL
# --------------------------------------------------
ard_connected = st.session_state.arduino_controller.is_connected

st.markdown(f"""
<div class="app-header">
    <div class="brand-container">
        <div class="brand-logo-box">
            <svg viewBox="0 0 24 24">
                <path d="M12 3L1 9l11 6 9-4.91V17h2V9L12 3zM3.82 9L12 4.54 20.18 9 12 13.46 3.82 9zM5 14.12v3.76l7 3.82 7-3.82v-3.76l-7 3.82-7-3.82z"/>
            </svg>
        </div>
        <div>
            <div class="brand-title">
                CLASSMATE
                <span class="brand-tag">ACCESSIBILITY AI</span>
            </div>
            <div class="brand-subtitle">AI-Powered Classroom Accessibility Companion</div>
        </div>
    </div>
    <div class="header-status-group">
        <div class="status-badge">
            <span class="status-dot"></span> System Active
        </div>
        <div class="status-badge {'status-badge' if ard_connected else 'status-badge-offline'}">
            <span class="{'status-dot' if ard_connected else 'status-dot-offline'}"></span> 
            Hardware {'Connected' if ard_connected else 'Offline'}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 1. CLASSROOM AUDIO INPUT SECTION
# --------------------------------------------------
st.markdown('<div class="panel-title">CLASSROOM AUDIO</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-description">Capture live classroom speech or upload recorded audio to analyze accessibility events.</div>', unsafe_allow_html=True)

tab_rec, tab_up = st.tabs(["Record Audio", "Upload Audio File"])

with tab_rec:
    recorded_audio = st.audio_input("Record classroom speech", key="mic_audio_record")
    if recorded_audio is not None:
        audio_id = hash(recorded_audio.getvalue())
        if st.session_state.processed_audio_id != audio_id:
            st.session_state.processed_audio_id = audio_id
            process_audio_bytes(recorded_audio.getvalue(), source_name="microphone")

with tab_up:
    uploaded_file = st.file_uploader("Select classroom audio file", type=["wav", "mp3", "m4a", "ogg"], key="upload_audio_file")
    if uploaded_file is not None:
        file_id = hash(uploaded_file.getvalue())
        if st.session_state.processed_audio_id != file_id:
            st.session_state.processed_audio_id = file_id
            st.audio(uploaded_file)
            process_audio_bytes(uploaded_file.getvalue(), source_name="file_upload")

st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)


# --------------------------------------------------
# 2. LIVE TRANSCRIPT & 3. INTELLIGENCE SECTION
# --------------------------------------------------
res = st.session_state.current_result

# LIVE TRANSCRIPT PANEL
st.markdown('<div class="panel-title">LIVE TRANSCRIPT</div>', unsafe_allow_html=True)
if res and res.get('original_transcript'):
    st.markdown(f'<div class="transcript-box">"{res.get("original_transcript")}"</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="transcript-box transcript-placeholder">Waiting for classroom audio...</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

# INTELLIGENCE / UNDERSTANDING SECTION
if res is not None:
    c_intel1, c_intel2 = st.columns(2)
    
    event_type = res.get("event_type", "NORMAL_LECTURE")
    p_code = res.get("priority", "P3")
    p_label = res.get("priority_label", "Normal")
    
    # Event Explanation Mapping
    event_explanations = {
        "DIRECT_ADDRESS": "Student has been directly addressed by the instructor.",
        "QUESTION": "A classroom question has been asked.",
        "ANNOUNCEMENT": "An important classroom or assignment announcement.",
        "INSTRUCTION": "Direct classroom instruction provided.",
        "EMERGENCY_ALARM": "Critical emergency alert detected.",
        "CLASS_BELL": "Classroom schedule bell sounded.",
        "NORMAL_LECTURE": "Standard classroom lecture audio."
    }
    explanation = event_explanations.get(event_type, "Classroom speech event processed.")
    
    with c_intel1:
        st.markdown(f"""
        <div class="panel-card" style="margin-bottom: 0;">
            <div class="panel-title">DETECTED EVENT</div>
            <div class="intel-title">{event_type.replace('_', ' ').title()}</div>
            <div class="intel-desc">{explanation}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c_intel2:
        st.markdown(f"""
        <div class="panel-card" style="margin-bottom: 0;">
            <div class="panel-title">PRIORITY</div>
            <div style="margin-top: 8px;">
                <span class="priority-pill badge-{p_code}">{p_code} &nbsp;·&nbsp; {p_label.upper()}</span>
            </div>
            <div class="intel-desc" style="margin-top: 10px;">Assigned priority based on student accessibility rules.</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # --------------------------------------------------
    # 4. ACCESSIBILITY ALERT (PRIMARY FOCAL POINT)
    # --------------------------------------------------
    headline_map = {
        "DIRECT_ADDRESS": "YOU WERE ADDRESSED",
        "EMERGENCY_ALARM": "CRITICAL EMERGENCY ALERT",
        "QUESTION": "INSTRUCTOR QUESTION ASKED",
        "ANNOUNCEMENT": "CLASSROOM ANNOUNCEMENT",
        "CLASS_BELL": "PERIOD BELL SOUNDED",
        "INSTRUCTION": "INSTRUCTION GIVEN"
    }
    headline = headline_map.get(event_type, "ACCESSIBILITY NOTIFICATION")
    
    alert_card_class = "alert-hero-card"
    if p_code == "P0":
        alert_card_class += " p0-alert"
    elif p_code == "P1":
        alert_card_class += " p1-alert"

    st.markdown(f"""
    <div class="{alert_card_class}">
        <div class="alert-label">ACCESSIBILITY ALERT</div>
        <div class="alert-headline">{headline}</div>
        <div class="alert-message">"{res.get('concise_message', 'No message')}"</div>
        <div class="alert-meta">
            <span class="priority-pill badge-{p_code}">{p_code} &nbsp;·&nbsp; {p_label.upper()}</span>
            <span class="alert-haptic-info">{res.get('haptic_pattern', '')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_act1, c_act2 = st.columns([1, 4])
    with c_act1:
        if st.button("Repeat Alert", use_container_width=True):
            st.session_state.arduino_controller.send_event_command(res)
            st.toast("Alert signal resent to hardware device.")

    st.markdown("<div style='margin-bottom: 32px;'></div>", unsafe_allow_html=True)


# --------------------------------------------------
# 5. RECENT CLASSROOM EVENTS HISTORY
# --------------------------------------------------
st.markdown('<div class="panel-title">RECENT CLASSROOM EVENTS</div>', unsafe_allow_html=True)

recent_events = st.session_state.event_logger.get_recent_events(limit=8)

if recent_events:
    st.markdown("""
    <div class="history-row history-header">
        <div>TIME</div>
        <div>EVENT</div>
        <div>PRIORITY</div>
        <div>MESSAGE</div>
    </div>
    """, unsafe_allow_html=True)
    
    for evt in recent_events:
        p_c = evt.get('priority', 'P3')
        st.markdown(f"""
        <div class="history-row">
            <div class="history-time">{evt.get('timestamp')}</div>
            <div class="history-event">{evt.get('event', '').replace('_', ' ').title()}</div>
            <div><span class="priority-pill badge-{p_c}">{p_c}</span></div>
            <div style="color: #c9d1d9; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">"{evt.get('message')}"</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    if st.button("Clear Event History"):
        st.session_state.event_logger.clear_events()
        st.session_state.current_result = None
        st.rerun()
else:
    st.markdown('<div class="panel-card" style="color: #6e7681; font-style: italic; text-align: center; padding: 24px;">No classroom events logged yet.</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 32px;'></div>", unsafe_allow_html=True)


# --------------------------------------------------
# 6. PRESET CLASSROOM EVENTS / TRIGGER CARDS
# --------------------------------------------------
st.markdown('<div class="panel-title">CLASSROOM EVENTS</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-description">Test accessibility responses against standard classroom situations.</div>', unsafe_allow_html=True)

classroom_preset_map = [
    {"id": "1", "label": "Student Addressed", "desc": "Direct name callout in lecture"},
    {"id": "2", "label": "Question", "desc": "Open question to classroom"},
    {"id": "3", "label": "Announcement", "desc": "Assignment submission deadline"},
    {"id": "5", "label": "Class Bell", "desc": "Schedule bell audio signal"},
    {"id": "6", "label": "Emergency Alert", "desc": "Emergency alarm audio signal"},
]

cols = st.columns(5)
for idx, preset in enumerate(classroom_preset_map):
    with cols[idx]:
        if st.button(preset["label"], key=f"btn_evt_{preset['id']}", use_container_width=True, help=preset["desc"]):
            result = demo_runner.run_scenario(preset['id'])
            st.session_state.current_result = result["pipeline_output"]
            st.session_state.current_result["original_transcript"] = result["raw_input"]
            st.rerun()

st.markdown("<div style='margin-bottom: 32px;'></div>", unsafe_allow_html=True)


# --------------------------------------------------
# 7. HARDWARE STATUS & DIAGNOSTICS (SUBTLE DRAWER)
# --------------------------------------------------
with st.expander("Hardware Diagnostics"):
    st.markdown(f"**Controller Status:** `{'Connected' if ard_connected else 'Offline'}`")
    avail_ports = ArduinoController.list_available_ports()
    c_p1, c_p2 = st.columns([3, 1])
    with c_p1:
        sel_port = st.selectbox("Serial Interface Port", options=["Select Port"] + avail_ports, label_visibility="collapsed")
    with c_p2:
        if not ard_connected:
            if st.button("Connect Device", use_container_width=True):
                if sel_port != "Select Port":
                    if st.session_state.arduino_controller.connect(sel_port):
                        st.success(f"Connected to {sel_port}")
                        st.rerun()
                    else:
                        st.error("Connection failed.")
        else:
            if st.button("Disconnect", use_container_width=True):
                st.session_state.arduino_controller.disconnect()
                st.info("Device disconnected.")
                st.rerun()
