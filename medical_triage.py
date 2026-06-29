HIGH_RISK_KEYWORDS = [
    "chest pain",
    "difficulty breathing",
    "can't breathe",
    "blood vomiting",
    "vomiting blood",
    "stroke",
    "heart attack",
    "unconscious",
    "seizure",
    "severe bleeding",
    "fainted",
    "loss of consciousness",
    "suicidal",
]

MEDIUM_RISK_KEYWORDS = [
    "high fever",
    "persistent fever",
    "severe headache",
    "eye pain",
    "vision loss",
    "burn",
    "fracture",
    "broken bone",
    "swollen face",
    "infection",
]

LOW_RISK_KEYWORDS = [
    "acne",
    "pimple",
    "rash",
    "itching",
    "dry skin",
    "cold",
    "cough",
]


def analyze_severity(text):

    text = text.lower()

    for word in HIGH_RISK_KEYWORDS:
        if word in text:
            return (
                "🔴 HIGH",
                "Seek immediate medical attention."
            )

    for word in MEDIUM_RISK_KEYWORDS:
        if word in text:
            return (
                "🟠 MEDIUM",
                "Medical consultation recommended."
            )

    return (
        "🟢 LOW",
        "Monitor symptoms and seek care if they worsen."
    )