chat_history = {}


def add_message(conversation_id, role, content):

    if conversation_id not in chat_history:
        chat_history[conversation_id] = []

    chat_history[conversation_id].append(
        f"{role}: {content}"
    )


def get_history(conversation_id):

    if conversation_id not in chat_history:
        return ""

    return "\n".join(
        chat_history[conversation_id]
    )