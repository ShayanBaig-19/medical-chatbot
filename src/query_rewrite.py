
from langchain_mistralai import ChatMistralAI
import os
from dotenv import load_dotenv

load_dotenv()


def rewrite_query(chat_history, query):

    llm = ChatMistralAI(
        api_key=os.getenv("mistral"),
        model="mistral-large-latest",
        temperature=0
    )


    prompt = f"""
    Given the conversation history and the new question,
    rewrite the question into a complete standalone question.

    History:
    {chat_history}

    Question:
    {query}

    Standalone question:
    """

    response = llm.invoke(prompt)

    return response.content