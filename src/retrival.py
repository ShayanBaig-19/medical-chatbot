#all imports
import os
from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from pinecone import Pinecone

load_dotenv()

def connect_pinecone():
    pinecone_client = Pinecone(
    api_key=os.getenv("Pinecone_key")
    )

    index = pinecone_client.Index("medical-chatbot-data")
    return index


def create_embeddings(query):
    client = MistralAIEmbeddings(
        model="mistral-embed",
        api_key=os.getenv("mistral")
    )
    return client.embed_query(query)

def retrieve_documents(query):

    index = connect_pinecone()

    embedding = create_embeddings(query)

    results = index.query(
        vector=embedding,
        top_k=3,
        include_metadata=True
    )

    return results



