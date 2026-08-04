from src.retrival import retrieve_documents
from src.llm import generate_response

query = input("Enter your question: ")

context = retrieve_documents(query)

answer = generate_response(context, query)

print(answer.content)