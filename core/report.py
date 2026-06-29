from report_generator import generate_medical_report


DEFAULT_REPORT = "medical_report.pdf"


def generate_report(
    patient_text,
    doctor_response,
    output_path=DEFAULT_REPORT
):
    """
    PDF Report Wrapper
    """

    if patient_text is None:
        patient_text = ""

    if doctor_response is None:
        doctor_response = ""

    try:

        report_path = generate_medical_report(

            patient_text=patient_text,

            doctor_response=doctor_response,

            output_path=output_path

        )

        return report_path

    except Exception as e:

        print(f"[REPORT ERROR] {e}")

        return None


def generate_report_safe(
    patient_text,
    doctor_response,
    output_path=DEFAULT_REPORT
):

    try:

        return generate_report(
            patient_text,
            doctor_response,
            output_path
        )

    except Exception:

        return None


def health_check():

    try:

        generate_report(
            "Test Patient",
            "Test Doctor Response"
        )

        return True

    except Exception:

        return False


if __name__ == "__main__":

    report = generate_report(

        patient_text="I have headache.",

        doctor_response="Take proper rest and drink enough water."

    )

    print(report)