from voice_of_the_doctor import text_to_speech_with_gtts


DEFAULT_OUTPUT = "final.mp3"


def speak(
    text,
    output_path=DEFAULT_OUTPUT
):
    """
    Text -> Speech Wrapper
    """

    if text is None:
        return None

    text = str(text).strip()

    if len(text) == 0:
        return None

    try:

        text_to_speech_with_gtts(

            input_text=text,

            output_filepath=output_path

        )

        return output_path

    except Exception as e:

        print(f"[TTS ERROR] {e}")

        return None


def speak_safe(
    text,
    output_path=DEFAULT_OUTPUT
):

    try:

        return speak(
            text,
            output_path
        )

    except Exception:

        return None


def health_check():

    try:

        return True

    except Exception:

        return False


if __name__ == "__main__":

    speak(
        "Hello. Your medical report is ready."
    )