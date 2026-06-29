from medical_triage import analyze_severity


def predict_severity(
    patient_text
):
    """
    Predict patient severity.
    """

    if patient_text is None:
        patient_text = ""

    try:

        severity, recommendation = analyze_severity(
            patient_text
        )

        return {

            "severity": severity,

            "recommendation": recommendation

        }

    except Exception as e:

        print(f"[SEVERITY ERROR] {e}")

        return {

            "severity": "Unknown",

            "recommendation": "Unable to determine severity."

        }


def predict_severity_safe(
    patient_text
):

    try:

        return predict_severity(
            patient_text
        )

    except Exception:

        return {

            "severity": "Unknown",

            "recommendation": "Unable to determine severity."

        }


def is_emergency(
    patient_text
):

    result = predict_severity(
        patient_text
    )

    severity = result["severity"].lower()

    emergency_keywords = [

        "critical",

        "emergency",

        "high",

        "severe"

    ]

    return any(
        word in severity
        for word in emergency_keywords
    )


def health_check():

    try:

        predict_severity(
            "I have fever"
        )

        return True

    except Exception:

        return False


if __name__ == "__main__":

    print(

        predict_severity(

            "I have chest pain and breathing difficulty."

        )

    )