import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    COLLECTION_NAME = "education"
    #MODEL_NAME = "mistral" #use this when using ollama
    MODEL_NAME = "mixtral-8x7b-32768"  # Related to the retrieval part
    DEBUG = os.getenv("DEBUG", "True").lower() in ['true', '1', 't']
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

config = Config()