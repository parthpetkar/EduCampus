import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

class Config:
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    COLLECTION_NAME = "chatbot"
    #MODEL_NAME = "mistral" #use this when using ollama
    MODEL_NAME = "llama-3.2-90b-text-preview"  # Related to the retrieval part
    DEBUG = os.getenv("DEBUG", "True").lower() in ['true', '1', 't']
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

config = Config()