# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# VoiceBot UI with Gradio

import os
import gradio as gr
print("1. Starting")

from dotenv import load_dotenv
print("2. dotenv loaded")

from core.conversation import clear_history
print("3. conversation loaded")

from core.consultation_manager import consultation_manager
print("4. consultation manager loaded")

from core.doctor_engine import doctor_engine
print("5. doctor engine loaded")

load_dotenv()
# Conversation Memory
conversation_history = []

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose.
What's in this image?. Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot,
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please. make the interface like gpt"""





# ---------------- UI ---------------- #
# -----------------------------
# Chat Handler
# -----------------------------

def send_message(

    patient_text,

    audio_filepath,

    image_filepath,

    history

):

    if history is None:

        history = []

    # -----------------------------
    # Validation
    # -----------------------------

    if (

        (patient_text is None or patient_text.strip() == "")

        and

        audio_filepath is None

    ):

        return (

            history,

            history,

            "",

            None,

            None

        )

    # -----------------------------
    # Doctor Engine
    # -----------------------------

    result = doctor_engine.run(

        patient_text=patient_text,

        audio_path=audio_filepath,

        image_path=image_filepath,

        system_prompt=system_prompt

    )
    print("=" * 50)
    print(result)
    print(type(result))
    print("=" * 50)

    # -----------------------------
    # Patient Bubble
    # -----------------------------

    history.append(

        {

            "role": "user",

            "content": result["patient"]

        }

    )

    # -----------------------------
    # Doctor Bubble
    # -----------------------------

    doctor_reply = result["doctor"]

    if isinstance(doctor_reply, dict):
        doctor_reply = doctor_reply.get("message", str(doctor_reply))

    history.append(
        {
            "role": "assistant",
            "content": doctor_reply
        }
    )

    # -----------------------------
    # Return
    # -----------------------------

    return (

        history,
        history,
        "",
        result.get("audio"),
        result.get("report")

    )


# -----------------------------
# Clear Chat
# -----------------------------

def clear_chat():

    # Backend Memory Reset
    clear_history()

    consultation_manager.reset()

    return (

        [],

        [],

        "",

        None,

        None

    )
# -----------------------------
# ChatGPT Style UI
# -----------------------------

CUSTOM_CSS = """
:root {
    --bg-main: #0b0f14;
    --bg-sidebar: #0b1117;
    --bg-card: #11161d;
    --border-color: #1f2937;
    --accent: #10b981;
    --accent-hover: #059669;
    --text-main: #e6edf3;
    --text-secondary: #9aa4b2;
    --bubble-doctor: #151b23;
    --bubble-user: #0f8a6f;
    --danger: #ef4444;
    --radius-btn: 12px;
    --radius-input: 14px;
    --radius-bubble: 16px;
}

* {
    font-family: 'Inter', system-ui, 'Segoe UI', Roboto, sans-serif !important;
}

/* Prevent fixed-box sizing from causing overflow/horizontal scroll
   at any zoom level or viewport size */
*, *::before, *::after {
    box-sizing: border-box;
}

html, body {
    overflow-x: hidden;
    height: 100%;
}

body, .gradio-container {
    background: radial-gradient(circle at 12% -10%, rgba(16,185,129,0.07), transparent 42%), var(--bg-main) !important;
    color: var(--text-main) !important;
    max-width: 100vw !important;
    height: 100vh;
    max-height: 100vh;
    overflow: hidden;
    margin: 0 !important;
    padding: 0 !important;
}

/* Gradio injects its own promo footer (Built with Gradio / API / Settings) —
   hide it so the custom UI fills the whole screen with no leftover gap */
.gradio-container footer{
    display: none !important;
}

/* Themed scrollbars for the sidebar / chat column instead of the default
   browser scrollbar, so internal scrolling still matches the dark theme */
#sidebar::-webkit-scrollbar,
#main-col::-webkit-scrollbar{
    width: 8px;
}
#sidebar::-webkit-scrollbar-track,
#main-col::-webkit-scrollbar-track{
    background: transparent;
}
#sidebar::-webkit-scrollbar-thumb,
#main-col::-webkit-scrollbar-thumb{
    background: #243042;
    border-radius: 8px;
}
#sidebar::-webkit-scrollbar-thumb:hover,
#main-col::-webkit-scrollbar-thumb:hover{
    background: var(--accent);
}
#sidebar, #main-col{
    scrollbar-width: thin;
    scrollbar-color: #243042 transparent;
}

/* Page shell: sidebar + main content, locked to the viewport on desktop so
   nothing needs to scroll except the two inner panes below */
#page-root {
    display: flex !important;
    flex-wrap: nowrap;
    width: 100%;
    height: 100vh;
    max-height: 100vh;
    overflow: hidden;
    align-items: stretch;
}

/* Top title */
#app-title h1 {
    font-size: clamp(20px, 1.4vw + 0.75rem, 28px);
    font-weight: 700;
    color: var(--text-main);
    margin: 0;
}

/* Sidebar */
#sidebar {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-color);
    padding: clamp(14px, 2vh, 20px) clamp(12px, 1.5vw, 16px);
    height: 100%;
    max-height: 100vh;
    flex: 0 0 clamp(220px, 19vw, 300px) !important;
    width: clamp(220px, 19vw, 300px) !important;
    max-width: clamp(220px, 19vw, 300px) !important;
    overflow-y: auto;
}

#sidebar-logo {
    font-size: clamp(16px, 1vw + 0.5rem, 18px);
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: clamp(14px, 2vh, 20px);
}

#new-consult-btn {
    background: var(--accent) !important;
    color: white !important;
    border-radius: var(--radius-btn) !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.30);
}

#new-consult-btn:hover {
    background: var(--accent-hover) !important;
}

#settings-btn {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-btn) !important;
    text-align: left !important;
}

#doctor-info-card {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-input) !important;
    padding: clamp(10px, 1.2vw, 14px) !important;
    margin-top: clamp(16px, 2.5vh, 24px);
}

/* ===========================================
   Sidebar Profile Card (NEW)
=========================================== */

.sidebar-profile {
    display: flex;
    align-items: center;
    gap: 12px;
}

.sidebar-avatar {
    flex: 0 0 auto;
    width: clamp(38px, 4vw, 46px);
    height: clamp(38px, 4vw, 46px);
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), #0ea5e9);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(18px, 2vw, 22px);
    box-shadow: 0 4px 14px rgba(16,185,129,0.35);
}

.sidebar-profile-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
}

.sidebar-profile-name {
    font-size: clamp(15px, 1.1vw, 17px);
    font-weight: 700;
    color: var(--text-main);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.sidebar-profile-role {
    font-size: 11px;
    color: var(--text-secondary);
    opacity: .85;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.sidebar-profile-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--text-secondary);
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 0 0 rgba(16,185,129,0.55);
    animation: status-pulse 2s infinite;
}

@keyframes status-pulse {
    0%   { box-shadow: 0 0 0 0 rgba(16,185,129,0.55); }
    70%  { box-shadow: 0 0 0 7px rgba(16,185,129,0); }
    100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
}

/* ===========================================
   Sidebar Quick Stats (NEW, demo data)
=========================================== */

.sidebar-stats {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-input);
    padding: clamp(10px, 1.2vw, 14px) clamp(6px, 1vw, 10px);
    margin: clamp(14px, 2vh, 20px) 0;
}

.stat-item {
    flex: 1 1 0;
    text-align: center;
    min-width: 0;
}

.stat-value {
    font-size: clamp(13px, 1vw, 15px);
    font-weight: 700;
    color: var(--accent);
    white-space: nowrap;
}

.stat-label {
    margin-top: 2px;
    font-size: 10px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: .04em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Subtle hover lift for sidebar buttons */
#new-consult-btn,
#settings-btn {
    transition: transform .2s ease, box-shadow .2s ease, background .2s ease, color .2s ease, border-color .2s ease;
}

#new-consult-btn:hover {
    transform: translateY(-1px);
}

#settings-btn:hover {
    border-color: var(--accent) !important;
    color: var(--text-main) !important;
    transform: translateY(-1px);
}

/* Sidebar footer (NEW) */
.sidebar-footer {
    margin-top: clamp(16px, 3vh, 28px);
    padding-top: clamp(10px, 1.5vh, 14px);
    border-top: 1px solid var(--border-color);
    font-size: 11px;
    color: var(--text-secondary);
    text-align: center;
    line-height: 1.4;
}

/* Header */
#header-row {
    border-bottom: 1px solid var(--border-color);
    padding: clamp(10px, 1.5vh, 14px) clamp(14px, 2vw, 24px);
    align-items: center;
    flex: 0 0 auto;
}

/* Main content column: header + chat + input stack and the chat
   area absorbs any extra/short viewport height */
#main-col {
    display: flex !important;
    flex-direction: column !important;
    flex: 1 1 auto !important;
    min-width: 0 !important;
    height: 100vh;
    max-height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
}

/* Chat area */
#chatbot {
    background: var(--bg-main) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-bubble) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.30);
    flex: 1 1 auto !important;
    height: auto !important;
    min-height: clamp(260px, 45vh, 600px) !important;
    max-height: none !important;
    width: 100% !important;
}

#chatbot .message.user {
    background: var(--bubble-user) !important;
    color: white !important;
    border-radius: var(--radius-bubble) !important;
}

#chatbot .message.bot {
    background: var(--bubble-doctor) !important;
    color: var(--text-main) !important;
    border-radius: var(--radius-bubble) !important;
}

/* Input bar */
/* Input Bar */
/* Input Bar */
/* Input Bar */
#input-bar{
    display:flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items:center !important;
    gap: clamp(8px, 1vw, 12px) !important;

    background:#11161d !important;
    border:1px solid var(--border-color) !important;
    border-radius:16px !important;

    padding: clamp(6px, 1vh, 8px) clamp(8px, 1.2vw, 12px) !important;
    height: auto !important;
    min-height: clamp(56px, 8vh, 64px) !important;
    flex: 0 0 auto !important;
    width: 100%;
    position: sticky;
    bottom: 0;
    z-index: 5;
}

/* Remove Gradio wrapper spacing */
#patient-textbox{
    margin:0 !important;
    padding:0 !important;
    min-height:auto !important;
    height:auto !important;
    flex: 1 1 auto !important;
    min-width: 0 !important;
}

/* Gradio internal textbox wrapper */
#patient-textbox > div{
    height: clamp(38px, 5vh, 46px) !important;
    min-height: clamp(38px, 5vh, 46px) !important;
    padding:0 !important;
    margin:0 !important;
}

/* Actual textarea */
#patient-textbox textarea{
    height: clamp(38px, 5vh, 46px) !important;
    min-height: clamp(38px, 5vh, 46px) !important;
    max-height: clamp(38px, 5vh, 46px) !important;

    padding: clamp(6px, 1vh, 10px) clamp(10px, 1.2vw, 14px) !important;
    margin:0 !important;

    line-height: 1.5 !important;
    font-size: clamp(13px, 0.5vw + 0.5rem, 15px);
    resize:none !important;
    overflow:hidden !important;
}

/* Send Button */
#send-btn{
    flex: 0 0 clamp(100px, 10vw, 150px) !important;
    width: clamp(100px, 10vw, 150px) !important;
    min-width: 100px !important;
    max-width: 150px !important;

    height: clamp(42px, 6vh, 50px) !important;
    border-radius:12px !important;
}

/* Bottom cards */
.bottom-card {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-input) !important;
    padding: clamp(12px, 1.5vw, 16px) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.30);
}

.bottom-card-title {
    font-size: clamp(14px, 1vw, 16px);
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 8px;
}

/* Voice + Image Row */

#voice-image-row{
    display:flex !important;
    align-items:stretch !important;
    gap: clamp(12px, 1.5vw, 18px);
    flex-wrap: wrap;
    flex: 0 0 auto;
    width: 100%;
    margin-top: clamp(10px, 1.5vh, 16px);
}

/* Left Card */

#voice-image-row > div:first-child{
    height: clamp(140px, 18vh, 180px) !important;
    flex: 1 1 240px;
    min-width: 220px;
}

/* Right Card */

#voice-image-row > div:last-child{
    height: clamp(140px, 18vh, 180px) !important;
    flex: 1 1 240px;
    min-width: 220px;
}

/* Voice Component */

#voice-image-row .gradio-audio{
    height:100% !important;
    min-height: clamp(140px, 18vh, 180px) !important;
}

/* Image Component */

#voice-image-row .gradio-image{
    height:100% !important;
    min-height: clamp(140px, 18vh, 180px) !important;
}

/* Upload Box */

#voice-image-row .upload-container{
    height: clamp(110px, 14vh, 150px) !important;
    min-height: clamp(110px, 14vh, 150px) !important;
}

/* Audio Box */

#voice-image-row .audio-container{
    height: clamp(110px, 14vh, 150px) !important;
    min-height: clamp(110px, 14vh, 150px) !important;
    overflow:visible !important;
}

/* Waveform */

#voice-image-row .waveform-container{
    min-height: clamp(50px, 8vh, 70px) !important;
}

/* Controls */

#voice-image-row .audio-controls{
    min-height: clamp(40px, 6vh, 50px) !important;
}

#clear-btn {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-btn) !important;
    flex: 0 0 auto;
}

#clear-btn:hover {
    color: var(--danger) !important;
    border-color: var(--danger) !important;
}

.online-dot {
    color: var(--accent);
    font-size: 12px;
}

/* ===========================================
   Bottom Cards
=========================================== */

.bottom-card{
    background:#11161d !important;
    border:1px solid #1f2937 !important;
    border-radius:18px !important;
    padding: clamp(14px, 1.8vw, 18px) !important;
    min-height: clamp(170px, 22vh, 230px) !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
    transition:.25s ease;
    overflow:hidden !important;
    position: relative;
}

.bottom-card::before{
    content:"";
    position:absolute;
    top:0; left:0; right:0;
    height:3px;
    background: linear-gradient(90deg, var(--accent), #0ea5e9);
    opacity:.85;
}

.bottom-card:hover{
    transform: translateY(-2px);
}

.bottom-card:hover{
    border-color:#10b981 !important;
    box-shadow:0 0 18px rgba(16,185,129,.18);
}

/* ===========================================
   Card Title
=========================================== */

.bottom-card-title{
    margin-bottom:14px !important;
    font-size: clamp(15px, 1.1vw, 18px) !important;
    font-weight:700 !important;
    color:#f3f4f6 !important;
}

/* ===========================================
   Audio Player
=========================================== */

.bottom-card audio{
    width:100% !important;
    height: clamp(44px, 6vh, 54px) !important;
    border-radius:12px !important;
}

/* Audio Container */

.bottom-card .audio-container{
    flex:1;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    background:#1b212b !important;
    border:1px solid #2c3746 !important;
    border-radius:14px !important;
    min-height: clamp(110px, 14vh, 150px) !important;
    padding: clamp(8px, 1vw, 12px) !important;
}

/* Hide label */

.bottom-card .audio-container label{
    display:none !important;
}

/* ===========================================
   File Component
=========================================== */

.bottom-card .file-wrap,
.bottom-card .file-preview,
.bottom-card .file-upload{
    background:#1b212b !important;
    border:1px dashed #374151 !important;
    border-radius:14px !important;
    min-height: clamp(110px, 14vh, 150px) !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    transition:.25s;
}

/* Hover */

.bottom-card .file-wrap:hover,
.bottom-card .file-upload:hover{
    border-color:#10b981 !important;
    background:#1d2633 !important;
}

/* File Button */

.bottom-card button{
    background:#10b981 !important;
    color:white !important;
    border:none !important;
    border-radius:10px !important;
    padding: clamp(8px, 1vh, 10px) clamp(14px, 1.5vw, 18px) !important;
    font-weight:600 !important;
    transition:.25s;
}

.bottom-card button:hover{
    background:#059669 !important;
}

/* Download Link */

.bottom-card a{
    color:#10b981 !important;
    text-decoration:none !important;
    font-weight:600 !important;
}

.bottom-card a:hover{
    color:#34d399 !important;
}

/* ===========================================
   Empty State
=========================================== */

.bottom-card .empty,
.bottom-card .placeholder{
    color:#9ca3af !important;
    font-size: clamp(13px, 0.9vw, 14px) !important;
}

/* ===========================================
   Responsive
=========================================== */

@media (max-width:1200px){

.bottom-card{
    min-height: clamp(150px, 20vh, 200px) !important;
}

.bottom-card .audio-container,
.bottom-card .file-wrap,
.bottom-card .file-preview{
    min-height: clamp(100px, 13vh, 130px) !important;
}

}

/* ===========================
   Mobile Responsive
=========================== */

@media (max-width:768px){

html, body, .gradio-container{
    height:auto !important;
    max-height:none !important;
    overflow:visible !important;
    overflow-x:hidden !important;
}

#page-root{
    flex-direction:column !important;
    height:auto !important;
    max-height:none !important;
    overflow:visible !important;
}

#sidebar{
    width:100% !important;
    min-width:100% !important;
    max-width:100% !important;
    flex: 0 0 auto !important;
    height:auto !important;
    max-height:none !important;
    overflow:visible !important;
    border-right:none !important;
    border-bottom:1px solid #1f2937;
    padding:16px !important;
}

#main-col{
    width:100% !important;
    height:auto !important;
    max-height:none !important;
    overflow:visible !important;
}

#chatbot{
    min-height:55vh !important;
}

#input-bar{
    flex-wrap:wrap !important;
    height:auto !important;
    position: static;
}

#patient-textbox{
    width:100% !important;
}

#send-btn{
    width:100% !important;
    max-width:100% !important;
    margin-top:10px;
}

#voice-image-row{
    flex-direction:column !important;
}

#voice-image-row > div{
    width:100% !important;
    height:auto !important;
    min-height:150px !important;
}

.bottom-card{
    width:100% !important;
    margin-top:15px;
}

}
"""

with gr.Blocks(
    title="AI Doctor",
    css=CUSTOM_CSS,
    theme=gr.themes.Base()
) as demo:

    with gr.Row(elem_id="page-root"):

        # -----------------------------
        # LEFT SIDEBAR
        # -----------------------------
        with gr.Column(scale=1, min_width=260, elem_id="sidebar"):

            gr.HTML(
                """
                <div class="sidebar-profile">
                    <div class="sidebar-avatar">🩺</div>
                    <div class="sidebar-profile-info">
                        <div class="sidebar-profile-name">AI Doctor</div>
                        <div class="sidebar-profile-role">General Physician · AI</div>
                        <div class="sidebar-profile-status">
                            <span class="status-dot"></span>Online
                        </div>
                    </div>
                </div>
                """,
                elem_id="sidebar-logo"
            )

            new_consult_btn_visual = gr.Button(
                "➕ New Consultation",
                elem_id="new-consult-btn"
            )

            settings_btn_visual = gr.Button(
                "⚙️ Settings",
                elem_id="settings-btn"
            )

            gr.HTML(
                """
                <div class="sidebar-stats">
                    <div class="stat-item">
                        <div class="stat-value">128</div>
                        <div class="stat-label">Consults</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">4.9★</div>
                        <div class="stat-label">Rating</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">~2s</div>
                        <div class="stat-label">Response</div>
                    </div>
                </div>
                """,
                elem_id="sidebar-stats"
            )

            # ---------------- Doctor Voice ----------------

            with gr.Column(elem_id="doctor-voice-card"):

                gr.Markdown(
                    "🔊 **Doctor's Voice**",
                    elem_classes="bottom-card-title"
                )

                doctor_voice = gr.Audio(
                    label="Doctor Voice",
                    interactive=False,
                    show_label=False
                )

            # ---------------- Medical Report ----------------

            with gr.Column(elem_id="medical-report-card"):

                gr.Markdown(
                    "📄 **Medical Report**",
                    elem_classes="bottom-card-title"
                )

                medical_report = gr.File(
                    label="Medical Report",
                    show_label=False
                )      

            gr.HTML(
                '<div class="sidebar-footer">🔒 Educational demo · Not medical advice</div>',
                elem_id="sidebar-footer"
            )

        # -----------------------------
        # RIGHT CONTENT
        # -----------------------------
        with gr.Column(scale=4, elem_id="main-col"):

            # HEADER
            with gr.Row(elem_id="header-row"):
                gr.Markdown("## AI Doctor &nbsp; 🟢 Online", elem_id="app-title")

            # CHAT AREA
            chatbot = gr.Chatbot(
                label="Conversation",
                height=450,
                type="messages",
                elem_id="chatbot"
            )

            chat_state = gr.State([])

            # INPUT BAR
            with gr.Row(elem_id="input-bar"):

                patient_text = gr.Textbox(
                    placeholder="Describe your symptoms or concerns...",
                    lines=1,
                    max_lines=1,
                    show_label=False,
                    container=False,
                    elem_id="patient-textbox"
                )

                send_btn = gr.Button(
                    "➤ Send",
                    variant="primary",
                    scale=1,
                    elem_id="send-btn"
                )

            # VOICE / IMAGE INPUTS
            with gr.Row(elem_id="voice-image-row"):

                audio_input = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    label="Voice"
                )

                image_input = gr.Image(
                    type="filepath",
                    label="Medical Image"
                )

            # BOTTOM CARDS
            # with gr.Row():

                # with gr.Column(elem_classes="bottom-card"):
                #     gr.Markdown("🔊 **Doctor's Voice**", elem_classes="bottom-card-title")
                #     doctor_voice = gr.Audio(
                #         label="Doctor Voice",
                #         interactive=False,
                #         show_label=False
                #     )

                # with gr.Column(elem_classes="bottom-card"):
                #     gr.Markdown("📄 **Medical Report**", elem_classes="bottom-card-title")
                #     medical_report = gr.File(
                #         label="Medical Report",
                #         show_label=False
                #     )

            clear_btn = gr.Button("Clear", elem_id="clear-btn")

    # -----------------------------
    # Events
    # -----------------------------

    # Send Button
    send_btn.click(
        fn=send_message,
        inputs=[
            patient_text,
            audio_input,
            image_input,
            chat_state
        ],
        outputs=[
            chatbot,
            chat_state,
            patient_text,
            doctor_voice,
            medical_report
        ],
        queue=False
    )

    # Press Enter to Send
    patient_text.submit(
        fn=send_message,
        inputs=[
            patient_text,
            audio_input,
            image_input,
            chat_state
        ],
        outputs=[
            chatbot,
            chat_state,
            patient_text,
            doctor_voice,
            medical_report
        ],
        queue=False
    )

    clear_btn.click(
        fn=clear_chat,
        outputs=[
            chatbot,
            chat_state,
            patient_text,
            doctor_voice,
            medical_report
        ]
    )

    # Visual-only sidebar buttons (no backend logic attached, purely cosmetic
    # shortcuts that reuse the existing Clear functionality so nothing breaks)
    new_consult_btn_visual.click(
        fn=clear_chat,
        outputs=[
            chatbot,
            chat_state,
            patient_text,
            doctor_voice,
            medical_report
        ]
    )



# -----------------------------
# Launch
# -----------------------------

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    debug=True
)