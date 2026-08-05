import logging
from src import logger
from src.retrival import retrieve_documents
from src.llm import generate_response
from src.memory import add_message, get_history
from src.query_rewrite import rewrite_query


logger = logging.getLogger(__name__)

logger.info("Application started")


while True:

    query = input("You: ")

    if query == "exit":
        break

    chat_history = get_history()

    new_query = rewrite_query(chat_history, query)

    try:
        context = retrieve_documents(new_query)

    except Exception as e:
        logger.error(f"Retrieval error: {e}")
        context = ""

    answer = generate_response(
        context,
        query,
        chat_history
    )

    print("AI:", answer.content)

    add_message("user", query)
    add_message("assistant", answer.content)