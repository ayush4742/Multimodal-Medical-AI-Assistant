# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

import os
import base64

from groq import Groq

# Import ONLY the function
from rag.retriever import retrieve_medical_context

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Default Model
model = "meta-llama/llama-4-scout-17b-16e-instruct"


# ==========================================
# Convert Image -> Base64
# ==========================================

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# ==========================================
# Vision + Medical RAG
# ==========================================

def analyze_image_with_query(query, model, encoded_image):

    client = Groq()

    # -------- Retrieve Medical Context --------

    medical_context = retrieve_medical_context(query)

    # -------- Final Prompt --------

    final_prompt = f"""
You are an experienced medical doctor.

Use the medical knowledge below whenever it is relevant.
Do not copy it directly.
Use it only to improve your diagnosis.

==========================
MEDICAL KNOWLEDGE
==========================

{medical_context}

==========================
PATIENT QUERY
==========================

{query}

Based on both the patient's symptoms and image:

• Give the most likely diagnosis.
• Mention possible causes.
• Suggest home remedies.
• Mention precautions.
• Mention when the patient should consult a doctor.

Keep the answer short and professional.
"""

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": final_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                }
            ]
        }
    ]

    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return chat_completion.choices[0].message.content