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

with gr.Blocks(
    title="AI Doctor"
) as demo:

    gr.Markdown(
        "# 🩺 AI Doctor"
    )

    chatbot = gr.Chatbot(
        label="Conversation",
        height=500,
        type="messages"
    )

    chat_state = gr.State([])

    with gr.Row():

        patient_text = gr.Textbox(
            label="Patient Message",
            placeholder="Type your symptoms...",
            lines=2,
            scale=5
        )

        send_btn = gr.Button(
            "Send",
            variant="primary",
            scale=1
        )

    with gr.Row():

        audio_input = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Voice"
        )

        image_input = gr.Image(
            type="filepath",
            label="Medical Image"
        )

    with gr.Row():

        doctor_voice = gr.Audio(
            label="Doctor Voice",
            interactive=False
        )

        medical_report = gr.File(
            label="Medical Report"
        )

    clear_btn = gr.Button("Clear")

    # -----------------------------
    # Events
    # -----------------------------

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
        ]
    )

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
        ]
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

# -----------------------------
# Launch
# -----------------------------

demo.launch(
    debug=True
)