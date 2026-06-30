from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from core.doctor_engine import doctor_engine

app = FastAPI(title="AI Doctor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "AI Doctor Backend Running"}


@app.post("/chat")
async def chat(
    message: str = Form(""),
    image: UploadFile | None = File(default=None),
    audio: UploadFile | None = File(default=None),
):

    image_path = None
    audio_path = None

    if image is not None:
        image_path = os.path.join(
            UPLOAD_DIR,
            image.filename
        )

        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

    if audio is not None:
        audio_path = os.path.join(
            UPLOAD_DIR,
            audio.filename
        )

        with open(audio_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

    result = doctor_engine.run(

        patient_text=message,

        audio_path=audio_path,

        image_path=image_path,

        system_prompt=""

    )

    return result