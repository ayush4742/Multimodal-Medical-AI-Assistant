# Load Environment Variables
from dotenv import load_dotenv
load_dotenv()

import os
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs

# =====================================
# API KEY
# =====================================

ELEVENLABS_API_KEY = os.getenv("ELEVEN_API_KEY")

# =====================================
# gTTS (Google Text To Speech)
# =====================================

def text_to_speech_with_gtts(input_text, output_filepath):

    audio = gTTS(
        text=input_text,
        lang="en",
        slow=False
    )

    audio.save(output_filepath)

    return output_filepath


# =====================================
# ElevenLabs
# =====================================

def text_to_speech_with_elevenlabs(input_text, output_filepath):

    client = ElevenLabs(
        api_key=ELEVENLABS_API_KEY
    )

    audio = client.generate(
        text=input_text,
        voice="Bella",
        model="eleven_turbo_v2",
        output_format="mp3_22050_32"
    )

    elevenlabs.save(audio, output_filepath)

    return output_filepath


# =====================================
# Testing
# =====================================

if __name__ == "__main__":

    text = """
    Hello, this is AI Doctor speaking.
    """

    print("Testing gTTS...")
    text_to_speech_with_gtts(
        text,
        "gtts_test.mp3"
    )

    print("gTTS Success")

    if ELEVENLABS_API_KEY:

        print("Testing ElevenLabs...")

        text_to_speech_with_elevenlabs(
            text,
            "eleven_test.mp3"
        )

        print("ElevenLabs Success")

    else:

        print("ELEVEN_API_KEY not found.")