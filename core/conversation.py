from collections import deque


class ConversationMemory:

    def __init__(self, max_messages=20):

        self.max_messages = max_messages

        self.messages = deque(maxlen=max_messages)

    # -------------------------------------

    def add_message(self, role, message):

        if message is None:
            return

        message = str(message).strip()

        if not message:
            return

        self.messages.append({

            "role": role,

            "message": message

        })

    # -------------------------------------

    def get_history(self):

        history = []

        for item in self.messages:

            history.append(
                f"{item['role']}: {item['message']}"
            )

        return "\n".join(history)

    # -------------------------------------

    def get_messages(self):

        return list(self.messages)

    # -------------------------------------

    def last_message(self):

        if not self.messages:
            return None

        return self.messages[-1]

    # -------------------------------------

    def clear(self):

        self.messages.clear()

    # -------------------------------------

    def size(self):

        return len(self.messages)

    # -------------------------------------

    def is_empty(self):

        return len(self.messages) == 0


# ===================================================

conversation = ConversationMemory()


def add_message(role, message):

    conversation.add_message(
        role,
        message
    )


def get_history():

    return conversation.get_history()


def get_messages():

    return conversation.get_messages()


def clear_history():

    conversation.clear()


def history_size():

    return conversation.size()