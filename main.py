import logging
import uuid
from src import logger
from src.retrival import retrieve_documents
from src.llm import generate_response
from src.memory import add_message, get_history
from src.query_rewrite import rewrite_query
from fastapi import FastAPI
from pydantic import BaseModel



logger = logging.getLogger(__name__)
logger.info("Application started")



app = FastAPI()



class ChatRequest(BaseModel):
    query: str
    conversation_id: str | None = None

@app.post("/chat")
def chat(request: ChatRequest):

    conversation_id = request.conversation_id
    if conversation_id is None:
      conversation_id = str(uuid.uuid4())

    query = request.query

    chat_history = get_history(conversation_id)

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

    add_message(conversation_id,"user",query)
    add_message( conversation_id,"assistant", answer.content)

    return {
    "conversation_id": conversation_id,
    "answer": answer.content
}