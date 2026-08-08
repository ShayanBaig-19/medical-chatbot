from setuptools import find_packages, setup

setup(
    name="medical_chatbot",
    version="1.1.0",
    author="Mirza Muhammad Shayan Baig",
    packages=find_packages(),
    install_requires=[
       "pypdf",
       "langchain",
       "langchain-text-splitters",
       "langchain-mistralai",
       "ipykernel",
       "pinecone",
       "python-dotenv",
       "fastapi",
       "uvicorn",
       "pydantic"
    ]
)
