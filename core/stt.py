import os

from voice_of_the_patient import transcribe_with_groq


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DEFAULT_MODEL = "whisper-large-v3"


def speech_to_text(
    audio_path,
    model=DEFAULT_MODEL
):
    """
    Speech -> Text Wrapper
    """

    if audio_path is None:
        return ""

    try:

        text = transcribe_with_groq(

            GROQ_API_KEY=GROQ_API_KEY,

            audio_filepath=audio_path,

            stt_model=model

        )

        if text is None:
            return ""

        return text.strip()

    except Exception as e:

        print(f"[STT ERROR] {e}")

        return ""


def speech_to_text_safe(
    audio_path
):
    """
    Never throws exception.
    """

    try:

        return speech_to_text(audio_path)

    except Exception:

        return ""


def health_check():

    return GROQ_API_KEY is not None


if __name__ == "__main__":

    print(

        speech_to_text(
            "patient.wav"
        )

    )