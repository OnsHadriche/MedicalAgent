from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
from pinecone import Pinecone
from src.helper import load_pdf_files, text_splitter, download_embeddings
from dotenv import load_dotenv
import os

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
pinecone_api_key = PINECONE_API_KEY

pinecone_client = Pinecone(pinecone_api_key)
index_name = "medical-chatbot"

if not pinecone_client.has_index(index_name):
    pinecone_client.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    
index = pinecone_client.Index(index_name)
extracted_data = load_pdf_files("data")
chunks = text_splitter(extracted_data)
embedding = download_embeddings()
docsearch = PineconeVectorStore.from_documents(chunks, embedding, index_name=index_name)
