import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from src.prompt import prompt

load_dotenv()

def generate_response(context, query):

    llm = ChatMistralAI(
        api_key=os.getenv("mistral"),
        model="mistral-large-latest",
        temperature=0.8
    )

    chain = prompt_template | llm

    answer = chain.invoke({
        "context": context,
        "question": query
    })

    return answer