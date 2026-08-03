#all imports
import os
from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from pinecone import Pinecone

#now code from ipynb just create a functions so that work will be done in a single function call


load_dotenv()
print("Environment variables loaded successfully!")


def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents
documents = load_pdf("data/Medical_book.pdf")

print("PDF loaded successfully!")

def split_documents(documents):
    text_split = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=150
    )
    chunks = text_split.split_documents(documents)
    return chunks
chunks = split_documents(documents)
print("Documents split successfully!")


def create_embeddings(model):
    client = MistralAIEmbeddings(
        model="mistral-embed",
        api_key=os.getenv("mistral")
    )
    text = [chunk.page_content for chunk in model]
    vectors = client.embed_documents(text)
    return vectors
vectors = create_embeddings(chunks)
print("Embeddings created successfully!")


def connect_pinecone():
    pinecone_client = Pinecone(
        api_key=os.getenv("Pinecone_key")
    )
    index = pinecone_client.Index("medical-chatbot-data")
    return index
index = connect_pinecone()
print("Connected to Pinecone successfully!")


def prepare_records(pdf_chunks, embedding_vectors):
    records = []
    for i in range(len(pdf_chunks)):
        current_chunk = pdf_chunks[i]
        current_vector = embedding_vectors[i]
        metadata = current_chunk.metadata.copy()
        metadata["text"] = current_chunk.page_content
        record = {
            "id": "chunk-" + str(i),
            "values": current_vector,
            "metadata": metadata
        }
        records.append(record)
    return records
records = prepare_records(chunks, vectors)
print("Records prepared successfully!")

#use the following function to store the vectors in pinecone index

def store_vectors(index, records):
    print("Inside store_vectors")
    batch_size = 100

    for start in range(0, len(records), batch_size):
        batch = records[start:start + batch_size]
        index.upsert(vectors=batch)

store_vectors(index, records)

print("All vectors uploaded successfully!")
