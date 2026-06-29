from dotenv import load_dotenv
load_dotenv()

import os
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))

voices = client.voices.get_all()

for v in voices.voices:
    print(v.name)