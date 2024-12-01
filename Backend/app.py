from flask import Flask, jsonify, request # type: ignore
from api.retrieval import retrieval_blueprint
from api.generation import generation_blueprint
from api.chat_with_pdf import chat_blueprint
from config import config
from flask_cors import CORS # type: ignore
from werkzeug.utils import secure_filename # type: ignore
import os

app = Flask(__name__)
app.config.from_object(config)
CORS(app, supports_credentials=False)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Register the blueprints for modular routes
app.register_blueprint(retrieval_blueprint, url_prefix="/api/retrieval")
app.register_blueprint(generation_blueprint, url_prefix="/api/generation")
app.register_blueprint(chat_blueprint, url_prefix="/api/chat_with_pdf")

@app.route('/api/query', methods=['POST'])
def query():
    """
    Route to handle user choice between retrieval, generation, and chat with PDF modes.
    """
    query = request.form.get("query", "")
    uploaded_file = request.files.get("file")
    print(request.files)  # This should display all uploaded files

    if not query:
        return jsonify({"error": "No query provided."}), 400

    file_path = None
    if uploaded_file :
        # Save the uploaded file
        filename = secure_filename(uploaded_file.filename)
        upload_dir = './uploads'
        os.makedirs(upload_dir, exist_ok=True)  # Ensure the upload directory exists
        
        # Use os.path.join to construct the full file path
        file_path = os.path.join(upload_dir, filename).replace("\\", "/")

        # Save the uploaded file
        uploaded_file.save(file_path)
        # Call the chat_with_pdf endpoint
        response = app.test_client().post(
            '/api/chat_with_pdf/generate',
            json={"file": file_path, "query": query}
        ).get_data(as_text=True)
        print(response)
        return jsonify({"response": response}), 200
    else:
        # Call the text generation endpoint if no file is uploaded
        response = app.test_client().post(
            '/api/generation/generate',
            json={"query": query}
        ).get_data(as_text=True)
        print(response)
        return jsonify({"response": response}), 200

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
