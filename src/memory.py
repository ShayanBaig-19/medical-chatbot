chat_history = []

def add_message(role, content):
    chat_history.append(
        f"{role}: {content}"
    )


def get_history():
    return "\n".join(chat_history)