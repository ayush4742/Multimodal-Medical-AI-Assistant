class ConsultationManager:

    def __init__(self):

        self.reset()

    def reset(self):

        self.history = []

        self.question_count = 0

        self.max_questions = 5

    def add_patient(self, text):

        self.history.append(
            f"Patient: {text}"
        )

    def add_doctor(self, text):

        self.history.append(
            f"Doctor: {text}"
        )

        self.question_count += 1

    def get_history(self):

        return "\n".join(self.history)

    def should_finish(self):

        return self.question_count >= self.max_questions


consultation_manager = ConsultationManager()