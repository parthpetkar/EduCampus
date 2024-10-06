from flask import Flask, jsonify, request
from api.retrieval import retrieval_blueprint
from api.generation import generation_blueprint
# from api.processing import process_query_with_ner  # Import the NER processing function
from config import config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config)
CORS(app, supports_credentials=False)

# Register the blueprints for modular routes
app.register_blueprint(retrieval_blueprint, url_prefix="/api/retrieval")
app.register_blueprint(generation_blueprint, url_prefix="/api/generation")

@app.route('/api/query', methods=['POST'])
def query():
    """
    Route to handle user choice between retrieval, generation, and NER modes.
    """
    data = request.get_json()
    
    # mode = data.get("mode", "retrieval").lower()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No query provided."}), 400

    # if mode == "generation":
        # optimized_query, entities = process_query_with_ner(query)
    response = app.test_client().post('/api/generation/generate', json={"query": query}).get_data(as_text=True)
    return jsonify({"response": response}), 200
    
    # elif mode == "ner":
    #     # Process the query with NER models
    #     optimized_query, entities = process_query_with_ner(query)
    #     return jsonify({
    #         "optimized_query": optimized_query,
    #         "entities": entities
    #     }), 200

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
