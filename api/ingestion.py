from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
import os
from config import config
from concurrent.futures import ThreadPoolExecutor
import time
from functools import wraps

def create_collection_if_not_exists(client):
    """
    Creates the collection in Qdrant if it does not exist, or recreates it with the correct dimensionality.
    """
    try:
        collections = client.get_collections().collections
        if config.COLLECTION_NAME not in [col.name for col in collections]:
            client.create_collection(
                collection_name=config.COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"Collection {config.COLLECTION_NAME} created successfully.")
        else:
            print(f"Collection {config.COLLECTION_NAME} already exists.")
    except Exception as e:
        print(f"Failed to create collection: {e}")

def retry(exceptions, tries=3, delay=2, backoff=2):
    """
    Retry decorator to handle exceptions and retry the operation.
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    print(f"Retrying due to {e}. Attempts left: {mtries - 1}")
                    mtries -= 1
                    time.sleep(mdelay)
                    mdelay *= backoff
            raise Exception("Maximum retries reached")
        return f_retry
    return deco_retry

@retry((Exception,), tries=3, delay=5, backoff=2)
def process_pdf(pdf_file, client, embeddings, text_splitter):
    """
    Processes a single PDF file, splits it into chunks, and ingests it into Qdrant.
    """
    try:
        pdf_file_path = os.path.join('data', pdf_file)
        docs = PyPDFLoader(file_path=pdf_file_path).load()
        chunks = text_splitter.split_documents(docs)

        vector_store = QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=config.COLLECTION_NAME,
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY,
            force_recreate=True
        )
        print(f"Document {pdf_file} ingested successfully.")
    except Exception as e:
        print(f"Failed to process {pdf_file}: {e}")

def ingest():
    """
    Ingests all PDF files from the 'data' folder into the Qdrant collection.
    """
    data_folder = "data"
    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"Folder {data_folder} does not exist.")

    client = QdrantClient(url=config.QDRANT_URL, api_key=config.QDRANT_API_KEY, timeout=120)
    create_collection_if_not_exists(client)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=200)
    embeddings = FastEmbedEmbeddings()

    pdf_files = [f for f in os.listdir(data_folder) if f.endswith(".pdf")]
    batch_size = 3  # Adjust this according to your server's capacity

    for i in range(0, len(pdf_files), batch_size):
        batch = pdf_files[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            for pdf_file in batch:
                executor.submit(process_pdf, pdf_file, client, embeddings, text_splitter)
