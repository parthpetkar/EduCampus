import requests
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings
import numpy as np
from flask import Flask, request, jsonify
from config import config

app = Flask(__name__)

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Qdrant API endpoint
qdrant_client = QdrantClient(url=config.QDRANT_URL, api_key=config.QDRANT_API_KEY)
embeddings = FastEmbedEmbeddings()
vector_store = QdrantVectorStore(client=qdrant_client, collection_name=config.COLLECTION_NAME, embedding=embeddings)

def add_questions(questions):
    headers = {"content-type": "application/json"}
    embeddings = model.encode(questions)
    qdrant_url = f"{config.QDRANT_URL}/collections/{config.COLLECTION_NAME}/points"  # Define the Qdrant API endpoint URL
    data = [{"id": i, "vector": embedding, "payload": {"question": question}} for i, (embedding, question) in enumerate(zip(embeddings, questions))]
    response = requests.post(qdrant_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Error adding questions: {response.text}")

def search_questions(query, top_k=5):
    headers = {"content-type": "application/json"}
    query_embedding = model.encode([query])[0]
    qdrant_url = f"{config.QDRANT_URL}/collections/{config.COLLECTION_NAME}/points/search"  # Define the Qdrant API endpoint URL
    data = {"vector": query_embedding, "top": top_k}
    response = requests.post(qdrant_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Error searching questions: {response.text}")
        return []
    results = response.json()["result"]
    return [result["payload"]["question"] for result in results]

def autocomplete_question(query, previous_queries):
    suggested_questions = search_questions(query)
    most_similar_question = find_highest_similar_query(suggested_questions, previous_queries)
    return most_similar_question

def find_highest_similar_query(suggested_questions, previous_queries):
    current_embedding = model.encode(suggested_questions)
    previous_embeddings = model.encode(previous_queries)
    similarities = cosine_similarity(current_embedding, previous_embeddings)
    max_similarities = similarities.max(axis=1)
    most_similar_index = np.argmax(max_similarities)
    most_similar_question = suggested_questions[most_similar_index]
    return most_similar_question

@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    query = request.args.get('query')
    previous_queries = request.args.getlist('previous_queries[]')
    autocomplete_result = autocomplete_question(query, previous_queries)
    return jsonify({'autocomplete_result': autocomplete_result})

if __name__ == '__main__':
    app.run(debug=True)