# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# VoiceBot UI with Gradio

import os
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

from report_generator import generate_medical_report
from medical_triage import analyze_severity   # <-- NEW

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts

# Conversation Memory
conversation_history = []

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose.
What's in this image?. Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot,
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath):

    global conversation_history

    # Safety Check
    if audio_filepath is None:
        return (
            "Please record your voice first.",
            "",
            None,
            None
        )

    # Speech → Text
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    # Store patient's message
    conversation_history.append(
        f"Patient: {speech_to_text_output}"
    )

    # Keep last 6 messages
    conversation_history = conversation_history[-6:]

    history = "\n".join(conversation_history)

    prompt = f"""
Previous Conversation:
{history}

Current Patient Message:
{speech_to_text_output}

{system_prompt}
"""

    # Vision Analysis
    if image_filepath:

        doctor_response = analyze_image_with_query(
            query=prompt,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )

    else:

        doctor_response = "No image provided for me to analyze."

    # ------------------ NEW FEATURE ------------------

    severity, advice = analyze_severity(
        speech_to_text_output
    )

    doctor_response += f"""

----------------------------------------

Severity : {severity}

Recommendation :
{advice}
"""

    # -------------------------------------------------

    # Save doctor's response in memory
    conversation_history.append(
        f"Doctor: {doctor_response}"
    )

    # Generate PDF Report
    report_path = generate_medical_report(
        speech_to_text_output,
        doctor_response
    )

    # Text → Speech
    text_to_speech_with_gtts(
        input_text=doctor_response,
        output_filepath="final.mp3"
    )

    return (
        speech_to_text_output,
        doctor_response,
        "final.mp3",
        report_path
    )


# ---------------- UI ---------------- #

iface = gr.Interface(
    fn=process_inputs,

    inputs=[
        gr.Audio(
            sources=["microphone"],
            type="filepath"
        ),
        gr.Image(
            type="filepath"
        )
    ],

    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor Voice"),
        gr.File(label="Medical Report")
    ],

    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)

# http://127.0.0.1:7860