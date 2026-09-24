CLASSMATE — PROFESSIONAL PRODUCT UI REDESIGN
UI/UX ONLY — PRESERVE ALL FUNCTIONALITY

You are redesigning the existing CLASSMATE application as a
professional, production-quality accessibility technology product.

IMPORTANT:
The current backend and functionality are already working.

DO NOT rewrite or modify the application logic.

DO NOT modify:
- Microphone recording
- Audio processing
- Faster-Whisper
- Speech-to-text
- Context detection
- Priority detection
- Event processing
- Event history logic
- Sound classification
- Arduino logic
- Serial communication
- Existing buttons' functionality
- Existing Python processing functions

ONLY redesign the frontend/UI and visual presentation.

Before changing anything, inspect the existing application and
understand the current layout and available functionality.

==================================================
1. PRODUCT IDENTITY
==================================================

Product name:

CLASSMATE

Subtitle:

AI-Powered Classroom Accessibility Companion

Brand personality:

- Intelligent
- Calm
- Professional
- Inclusive
- Reliable
- Modern
- Human-centered

The application should feel like a real accessibility technology
product, not a college project or generic AI dashboard.

Avoid the visual language of:
- Generic AI dashboards
- SaaS admin panels
- Developer tools
- Streamlit default interfaces
- Hackathon templates

==================================================
2. VISUAL DIRECTION
==================================================

Use a refined dark interface.

Design inspiration:

- Linear
- Notion
- Arc
- Modern accessibility technology products
- Premium productivity applications

Do NOT copy any specific website.

Use:

- Deep neutral background
- Slightly lighter surfaces
- Off-white primary text
- Muted secondary text
- One restrained accent color
- Subtle borders
- Soft shadows
- Clear spacing
- Strong typography
- Minimal icons

Avoid:

- Purple/blue AI gradients
- Neon colors
- Excessive glassmorphism
- Huge glowing effects
- Excessive rounded cards
- Excessive animations
- Emoji-heavy UI
- Decorative elements with no purpose

The interface should feel sophisticated rather than flashy.

==================================================
3. LAYOUT
==================================================

Create a strong application shell.

TOP HEADER:

CLASSMATE
AI-Powered Classroom Accessibility Companion

Right side:

● System Active

Keep the header compact.

==================================================
4. PRIMARY EXPERIENCE
==================================================

The most important thing on the screen is the classroom
accessibility workflow.

Structure the page visually as:

CLASSROOM AUDIO
        ↓
LIVE TRANSCRIPT
        ↓
UNDERSTANDING
        ↓
PRIORITY
        ↓
ACCESSIBILITY ALERT

However, do NOT literally make it look like a flowchart.

Use spacing, section hierarchy and subtle visual connectors
to communicate the progression.

==================================================
5. AUDIO SECTION
==================================================

Create a premium audio input card.

Title:

CLASSROOM AUDIO

Supporting text:

Capture classroom speech and identify important events.

Keep the EXISTING working recording functionality.

The primary button should be visually dominant:

[  ●  Record classroom audio  ]

When recording:

[  ■  Stop recording  ]

Use a subtle recording indicator.

Do NOT create fake microphone states.

Only show a recording state when the actual recorder is active.

Also retain the existing upload functionality if it already works.

==================================================
6. TRANSCRIPT SECTION
==================================================

Create a large, elegant transcript panel.

Label:

LIVE TRANSCRIPT

Display the REAL Faster-Whisper result.

Example:

"Jeeva, can you come to the board?"

Make this the largest piece of content after the main heading.

If no transcript exists:

Waiting for classroom audio...

Do not display fake transcript content by default.

==================================================
7. INTELLIGENCE SECTION
==================================================

Create a clean two-column layout.

LEFT:

DETECTED EVENT

DIRECT ADDRESS

Supporting explanation:

Student has been directly addressed.

RIGHT:

PRIORITY

P1

DIRECTLY RELEVANT

The priority should have strong visual hierarchy.

P0 = critical
P1 = directly relevant
P2 = important
P3 = informational

Use the existing priority value dynamically.

Do not hard-code example values.

==================================================
8. ACCESSIBILITY ALERT
==================================================

This should be the visual focal point of the lower half of the
screen.

Create a premium accessibility alert card.

Label:

ACCESSIBILITY ALERT

Main message:

YOU WERE ADDRESSED

Secondary message:

"Please come to the board."

Below:

P1 · DIRECTLY RELEVANT

[ Repeat message ]

The alert must use the existing generated message.

Do not hard-code the example.

Make this section feel like the actual output delivered to
the student.

==================================================
9. EVENT HISTORY
==================================================

Create a clean, compact event timeline.

Title:

RECENT CLASSROOM EVENTS

Each row:

TIME | EVENT | PRIORITY | MESSAGE

Example styling:

09:42
Direct Address
P1
"Please come to the board."

Keep the event history visually compact.

Do not fill it with fake events.

If empty:

No classroom events yet.

Use the existing event history data.

==================================================
10. CLASSROOM EVENTS / SCENARIOS
==================================================

If the current application contains the five existing event
triggers, redesign them as professional classroom event cards.

Use:

Student Addressed
Question
Announcement
Class Bell
Emergency Alert

Do NOT call this:

Demo Mode
Simulation
Test Mode
Hackathon Mode

Do NOT display numbers such as 1, 2, 3, 4, 5 to the user.

The underlying functionality must remain exactly the same.

==================================================
11. HARDWARE STATUS
==================================================

If hardware status is already available, show it subtly.

Example:

HARDWARE
● Connected

or

HARDWARE
○ Offline

Do not expose:

COM port
baud rate
serial configuration
developer settings

on the primary interface.

==================================================
12. NAVIGATION
==================================================

If navigation is required, keep it minimal.

Use:

Overview
Classroom Events
Event History

Do not create unnecessary pages.

Do not duplicate functionality.

==================================================
13. TYPOGRAPHY
==================================================

Use a modern sans-serif typeface.

Hierarchy:

Product name → strong
Section headings → medium/semibold
Primary information → large
Supporting information → muted/small

Avoid excessive bold text.

Use consistent typography throughout the application.

==================================================
14. SPACING
==================================================

The current interface should NOT feel empty.

Use a structured max-width container.

Maintain:

- Consistent horizontal padding
- Consistent card spacing
- Clear vertical rhythm
- Balanced proportions

The main content should occupy the available screen naturally
without stretching cards unnecessarily.

Optimize for:

1366 × 768
1920 × 1080

Avoid horizontal scrolling.

==================================================
15. MICRO-INTERACTIONS
==================================================

Use subtle interactions only.

Examples:

- Record button changes state while recording
- Cards have subtle hover feedback
- Alert appears smoothly after processing
- Priority state updates cleanly
- Event history updates without visual clutter

Do NOT use flashy animations.

==================================================
16. PROFESSIONAL LANGUAGE
==================================================

Never display:

Demo
Prototype
Simulation
Educational purpose
Student project
Hackathon
Test mode
Mock
Sample
Development version

The interface should simply present CLASSMATE as a professional
accessibility product.

Do not expose implementation details such as:

Python
Streamlit
Faster-Whisper model name
internal module names
file paths
COM ports
debug information

These may remain in the code but should not appear in the
main product interface.

==================================================
17. RESPONSIVENESS
==================================================

The UI must remain clean at:

1366×768
1920×1080

Avoid excessive vertical scrolling.

The most important information should be visible without
requiring the user to scroll excessively.

==================================================
18. CRITICAL FUNCTIONALITY RULE
==================================================

THIS IS A FRONTEND REDESIGN.

Do not rewrite working backend code just to achieve the design.

After completing the UI redesign, verify:

1. Record Audio still works.
2. Microphone permission still works.
3. Faster-Whisper still generates the transcript.
4. Context detection still works.
5. Priority detection still works.
6. Accessibility alert still works.
7. Event history still updates.
8. Existing classroom event triggers still work.
9. Existing Arduino functionality is untouched.

If something breaks, restore the original functionality.

==================================================
FINAL DESIGN TEST
==================================================

When the application opens, the first impression should be:

"This is a real AI accessibility product."

NOT:

"This is a Streamlit application."

NOT:

"This is a college project."

NOT:

"This is a hackathon dashboard."

The final UI should be minimal, premium, professional,
accessible, and highly readable.

DO NOT add new product features.

DO NOT change the existing functionality.

ONLY improve the visual design, layout, hierarchy,
typography, spacing, interaction states and overall polish.