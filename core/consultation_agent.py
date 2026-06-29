import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are an experienced medical doctor conducting a consultation.

Your goal is NOT to diagnose immediately.

Your goal is to collect enough information before giving a diagnosis.

RULES:

1. Ask ONLY ONE medical question at a time.

2. Never repeat a question that has already been asked.

3. Remember previous patient answers.

4. Maximum follow-up questions: 5.

5. If enough information is available, stop asking questions.

Return ONLY valid JSON.

If more information is required:

{
  "action":"QUESTION",
  "message":"next medical question"
}

If diagnosis is possible:

{
  "action":"DIAGNOSIS",
  "message":"diagnosis with precautions and remedies"
}

If symptoms indicate emergency:

{
  "action":"EMERGENCY",
  "message":"Immediate emergency advice."
}

Never output markdown.

Never explain JSON.

Return JSON only.
"""


class ConsultationAgent:

    def __init__(self):

        self.max_questions = 5

    def decide(
        self,
        history
    ):

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0.2,

            response_format={
                "type": "json_object"
            },

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": history
                }

            ]

        )

        try:

            return json.loads(
                response.choices[0].message.content
            )

        except Exception:

            return {

                "action": "ERROR",

                "message": response.choices[0].message.content

            }


consultation_agent = ConsultationAgent()


def consultation_step(history):

    return consultation_agent.decide(history)