import json
from urllib import response

from core.stt import speech_to_text
from core.consultation_agent import consultation_step
from core.consultation_manager import consultation_manager
from core.rag import retrieve
from core.conversation import (
    add_message,
    get_history
)


from core.utils import build_prompt
from core.vision import analyze_image_safe

from core.severity import predict_severity

from core.report import generate_report

from core.tts import speak



class DoctorEngine:

    def __init__(self):

        print("AI Doctor Engine Loaded")

    def prepare_prompt(
        self,
        patient_text,
        system_prompt
    ):

        history = consultation_manager.get_history()

        medical_context = retrieve(
            patient_text
        )

        prompt = build_prompt(
            system_prompt,
            history,
            patient_text
        )

        final_prompt = f"""
{prompt}

=========================
MEDICAL KNOWLEDGE
=========================

{medical_context}
"""

        return final_prompt

    def run(
        self,
        audio_path=None,
        image_path=None,
        system_prompt="",
        patient_text=None
    ):

        # -----------------------------
        # Speech To Text
        # -----------------------------

        if patient_text is None or patient_text.strip() == "":

            patient_text = speech_to_text(
                audio_path
            )

        patient_text = patient_text.strip()

        # -----------------------------
        # Conversation Memory
        # -----------------------------

        add_message(
            "Patient",
            patient_text
        )
        consultation_manager.add_patient(
            patient_text
        )

        history = consultation_manager.get_history()
        # -----------------------------
        # Consultation Agent
        # -----------------------------

        decision = consultation_step(
            history
        )

        if not isinstance(decision, dict):

            return {

                "status": "ERROR",

                "patient": patient_text,

                "doctor": str(decision),

                "audio": None,

                "report": None,

                "severity": None,

                "recommendation": None

            }

        # -------------------------------------------------------
        # Follow-up Question
        # -------------------------------------------------------

        if decision["action"] == "QUESTION":

            consultation_manager.add_doctor(
                decision["message"]
            )

            add_message(
                "Doctor",
                decision["message"]
            )

            return {

                "status": "QUESTION",

                "patient": patient_text,

                "doctor": decision["message"],

                "audio": None,

                "report": None,

                "severity": None,

                "recommendation": None

            }


        # -------------------------------------------------------
        # Emergency Case
        # -------------------------------------------------------

        elif decision["action"] == "EMERGENCY":

            print("\n" + "="*60)
            print("ENTERED EMERGENCY BRANCH")
            print("="*60)

            doctor_response = decision["message"]

            print("Doctor Response:")
            print(doctor_response)

            severity = decision.get(
                "severity",
                "Emergency"
            )

            recommendation = decision.get(
                "recommendation",
                "Go to the nearest hospital immediately."
            )

            print("Severity:", severity)
            print("Recommendation:", recommendation)

            add_message(
                "Doctor",
                doctor_response
            )

            print("\nGenerating Report...")

            report_path = generate_report(
                patient_text,
                doctor_response
            )

            print("Report Path:", report_path)

            print("\nGenerating Voice...")
            print("Before Speak")
            audio_path = speak(
                doctor_response
            )
            print("After Speak")
            print(audio_path)

            print("Audio Path:", audio_path)

            consultation_manager.reset()

            print("\nReturning Response")
            print("="*60)

            return {

                "status": "EMERGENCY",

                "patient": patient_text,

                "doctor": doctor_response,

                "audio": audio_path,

                "report": report_path,

                "severity": severity,

                "recommendation": recommendation

            }
        # -----------------------------
        # Prepare Prompt
        # -----------------------------

        prompt = self.prepare_prompt(
            patient_text,
            system_prompt
        )

        # -----------------------------
        # Vision Analysis
        # -----------------------------

        doctor_response = decision["message"]

        if image_path:

            vision_response = analyze_image_safe(

                image_path,

                prompt

            )

            if vision_response:

                doctor_response = vision_response

        # -----------------------------
        # Severity Analysis
        # -----------------------------

        severity_result = predict_severity(

            patient_text

        )
        severity = severity_result["severity"]

        recommendation = severity_result["recommendation"]

        doctor_response += f"""

----------------------------------------

Severity : {severity}

Recommendation :

{recommendation}
"""

        # -----------------------------
        # Save Conversation
        # -----------------------------

        add_message(
            "Doctor",
            doctor_response
        )

        consultation_manager.reset()

        # -----------------------------
        # Generate Report
        # -----------------------------

        report_path = generate_report(

            patient_text,

            doctor_response

        )

        # -----------------------------
        # Text To Speech
        # -----------------------------
        print("Before Speak")
        audio_path = speak(
            doctor_response
        )
        print("After Speak")
        print(audio_path)

        # -----------------------------
        # Final Response
        # -----------------------------
        return {

            "status": "DIAGNOSIS",

            "patient": patient_text,

            "doctor": doctor_response,

            "audio": audio_path,

            "report": report_path,

            "severity": severity,

            "recommendation": recommendation

        }

doctor_engine = DoctorEngine()