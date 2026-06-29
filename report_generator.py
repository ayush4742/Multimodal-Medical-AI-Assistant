from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os


def generate_medical_report(patient_text, doctor_response, output_path="medical_report.pdf"):

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path)

    story = []

    story.append(Paragraph("<b>AI DOCTOR MEDICAL REPORT</b>", styles["Title"]))
    story.append(Paragraph(f"Generated On: {datetime.now()}", styles["Normal"]))

    story.append(Paragraph("<br/><b>Patient Symptoms</b>", styles["Heading2"]))
    story.append(Paragraph(patient_text, styles["BodyText"]))

    story.append(Paragraph("<br/><b>Doctor Assessment</b>", styles["Heading2"]))
    story.append(Paragraph(doctor_response, styles["BodyText"]))

    story.append(Paragraph("<br/><b>Disclaimer</b>", styles["Heading2"]))
    story.append(
        Paragraph(
            "This report is AI generated and should not replace consultation with a licensed medical professional.",
            styles["BodyText"]
        )
    )

    doc.build(story)

    return os.path.abspath(output_path)