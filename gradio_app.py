# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# VoiceBot UI with Gradio

import os
import gradio as gr
from dotenv import load_dotenv
from core.conversation import clear_history
from core.consultation_manager import consultation_manager

load_dotenv()

from core.doctor_engine import doctor_engine


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

body, .gradio-container {
    background: var(--bg-main) !important;
    color: var(--text-main) !important;
}

/* Top title */
#app-title h1 {
    font-size: 28px;
    font-weight: 700;
    color: var(--text-main);
    margin: 0;
}

/* Sidebar */
#sidebar {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-color);
    padding: 20px 16px;
    min-height: 100vh;
}

#sidebar-logo {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 20px;
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
    padding: 14px !important;
    margin-top: 24px;
}

/* Header */
#header-row {
    border-bottom: 1px solid var(--border-color);
    padding: 14px 24px;
    align-items: center;
}

/* Chat area */
#chatbot {
    background: var(--bg-main) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-bubble) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.30);
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
    align-items:center !important;
    gap:12px !important;

    background:#11161d !important;
    border:1px solid var(--border-color) !important;
    border-radius:16px !important;

    padding:8px 12px !important;
    height:64px !important;
    min-height:64px !important;
}

/* Remove Gradio wrapper spacing */
#patient-textbox{
    margin:0 !important;
    padding:0 !important;
    min-height:auto !important;
    height:auto !important;
}

/* Gradio internal textbox wrapper */
#patient-textbox > div{
    height:46px !important;
    min-height:46px !important;
    padding:0 !important;
    margin:0 !important;
}

/* Actual textarea */
#patient-textbox textarea{
    height:46px !important;
    min-height:46px !important;
    max-height:46px !important;

    padding:10px 14px !important;
    margin:0 !important;

    line-height:24px !important;
    resize:none !important;
    overflow:hidden !important;
}

/* Send Button */
#send-btn{
     flex:0 0 150px !important;
    width:150px !important;
    min-width:150px !important;
    max-width:150px !important;

    height:50px !important;
    border-radius:12px !important;
}

/* Bottom cards */
.bottom-card {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-input) !important;
    padding: 16px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.30);
}

.bottom-card-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 8px;
}

/* Voice + Image Row */

#voice-image-row{
    display:flex !important;
    align-items:stretch !important;
    gap:18px;
}

/* Left Card */

#voice-image-row > div:first-child{
    height:180px !important;
}

/* Right Card */

#voice-image-row > div:last-child{
    height:180px !important;
}

/* Voice Component */

#voice-image-row .gradio-audio{
    height:100% !important;
    min-height:180px !important;
}

/* Image Component */

#voice-image-row .gradio-image{
    height:100% !important;
    min-height:180px !important;
}

/* Upload Box */

#voice-image-row .upload-container{
    height:150px !important;
    min-height:150px !important;
}

/* Audio Box */

#voice-image-row .audio-container{
    height:150px !important;
    min-height:150px !important;
    overflow:visible !important;
}

/* Waveform */

#voice-image-row .waveform-container{
    min-height:70px !important;
}

/* Controls */

#voice-image-row .audio-controls{
    min-height:50px !important;
}

#clear-btn {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-btn) !important;
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
    padding:18px !important;
    min-height:230px !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
    transition:.25s ease;
    overflow:hidden !important;
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
    font-size:18px !important;
    font-weight:700 !important;
    color:#f3f4f6 !important;
}

/* ===========================================
   Audio Player
=========================================== */

.bottom-card audio{
    width:100% !important;
    height:54px !important;
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
    min-height:150px !important;
    padding:12px !important;
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
    min-height:150px !important;
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
    padding:10px 18px !important;
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
    font-size:14px !important;
}

/* ===========================================
   Responsive
=========================================== */

@media (max-width:1200px){

.bottom-card{
    min-height:200px !important;
}

.bottom-card .audio-container,
.bottom-card .file-wrap,
.bottom-card .file-preview{
    min-height:130px !important;
}

}

/* ===========================
   Mobile Responsive
=========================== */

@media (max-width:768px){

#page-root{
    flex-direction:column !important;
}

#sidebar{
    width:100% !important;
    min-width:100% !important;
    max-width:100% !important;
    height:auto !important;
    border-right:none !important;
    border-bottom:1px solid #1f2937;
    padding:16px !important;
}

#main-col{
    width:100% !important;
}

#chat-wrapper{
    height:55vh !important;
}

#input-bar{
    flex-wrap:wrap !important;
    height:auto !important;
}

#patient-textbox{
    width:100% !important;
}

#send-btn{
    width:100% !important;
    margin-top:10px;
}

#voice-image-row{
    flex-direction:column !important;
}

#voice-image-row > div{
    width:100% !important;
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

    with gr.Row():

        # -----------------------------
        # LEFT SIDEBAR
        # -----------------------------
        with gr.Column(scale=1, min_width=260, elem_id="sidebar"):

            gr.Markdown(
                "🩺 **AI Doctor**  \n🟢 Online",
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

            gr.Markdown("&nbsp;")

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

        # -----------------------------
        # RIGHT CONTENT
        # -----------------------------
        with gr.Column(scale=4):

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