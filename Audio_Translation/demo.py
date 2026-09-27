from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

audio_file = open("tts-audio.mp3", "rb")

output = client.audio.transcriptions.create(
    model="whisper-large-v3",
    file=audio_file
)

print(output.text)