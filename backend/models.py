from pydantic import BaseModel


class DiagnosisResponse(BaseModel):
    speech_to_text: str
    doctor_response: str
    severity: str
    recommendation: str