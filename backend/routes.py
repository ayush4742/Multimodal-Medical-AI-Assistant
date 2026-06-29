from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "Backend Running",
        "model": "AI Doctor v2"
    }


@router.post("/diagnosis")
async def diagnosis(
    image: UploadFile = File(...)
):

    os.makedirs("temp", exist_ok=True)

    image_path = f"temp/{image.filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {
        "message": "Image received successfully",
        "image_path": image_path
    }