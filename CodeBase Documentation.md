# VIT Chatbot System 

## Overview

The VIT Chatbot System is a Flask-based backend application with a Vue.js frontend that provides intelligent responses to queries about Vishwakarma Institute of Technology (VIT), Pune. The system features PDF document processing, audio transcription, and context-aware responses using vector search and language models.

## System Architecture

### Backend Components

## 1. app.py

Main application file that initializes and configures the Flask application.

### Functions

#### `query()`

```python
@app.route('/api/query', methods=['POST'])
def query()
```

- **Purpose**: Main entry point for handling user queries
- **Parameters**: Accepts form data with:
    - `query`: Text string containing user's question
    - `file`: Optional PDF file upload
- **Process**:
    1. Validates query presence
    2. Handles file upload if present
    3. Routes to appropriate endpoint (chat_with_pdf or generation)
- **Returns**: JSON response with query results or error message
- **Error Handling**: Returns 400 for missing query

#### `audio()`

```python
@app.route('/api/upload_audio', methods=['POST'])
def audio()
```

- **Purpose**: Handles audio file uploads and transcription
- **Parameters**: Expects 'audio' file in request.files
- **Process**:
    1. Validates audio file presence
    2. Securely saves file
    3. Calls audio conversion endpoint
- **Returns**: JSON with transcription or error message
- **Error Handling**: Returns 400 for missing/empty files

## 2. audio_conversion.py

Handles audio file processing and transcription.

### Functions

#### `convert_audio_to_text()`

```python
@audio_blueprint.route('/convert', methods=['POST'])
def convert_audio_to_text()
```

- **Purpose**: Converts audio files to text using Groq API
- **Parameters**: JSON payload with:
    - `file`: Path to audio file
- **Process**:
    1. Validates file existence
    2. Opens and reads audio file
    3. Calls Groq API for transcription
- **Returns**: JSON with transcription text
- **Error Handling**:
    - 400 for file not found
    - 500 for transcription errors

## 3. chat_with_pdf.py

Manages PDF document processing and chat interactions.

### Functions

#### `generate()`

```python
@chat_blueprint.route('/generate', methods=['POST'])
def generate()
```

- **Purpose**: Processes PDF and generates responses
- **Parameters**: JSON payload with:
    - `file`: PDF file path
    - `query`: User question
- **Process**:
    1. Validates inputs
    2. Creates temporary collection
    3. Processes PDF content
    4. Retrieves relevant context
    5. Generates refined query
    6. Produces final response
- **Returns**: JSON with generated response
- **Error Handling**: Various error states with appropriate codes

#### `create_collection_if_not_exists(client)`

- **Purpose**: Manages Qdrant collection creation
- **Parameters**:
    - `client`: Qdrant client instance
- **Process**:
    1. Checks collection existence
    2. Creates if missing
    3. Configures vector parameters
- **Error Handling**: Logs creation failures

#### `process_file_data(file_path)`

- **Purpose**: Processes PDF files into document chunks
- **Parameters**:
    - `file_path`: Path to PDF file
- **Process**:
    1. Loads PDF content
    2. Creates document objects
    3. Adds metadata
- **Returns**: List of Document objects
- **Error Handling**: Raises ValueError for processing errors

## API Endpoints

### 1. Main Query Endpoint

```
POST /api/query
Form Data:
- query (required): User question
- file (optional): PDF file for context
```

### 2. Audio Processing

```
POST /api/audio_conversion/convert
JSON Body:
- file: Path to audio file
```

### 3. PDF Chat

```
POST /api/chat_with_pdf/generate
JSON Body:
- file: Path to PDF file
- query: User question
```

### 4. Text Generation

```
POST /api/generation/generate
JSON Body:
- query: User question
```

### 5. Document Retrieval

```
POST /api/retrieval/retrieve
JSON Body:
- query: Search query
```

## Deployment

### Requirements

```
Python 3.8+
Flask
Groq
Qdrant Client
LangChain
FastEmbed
PyPDF Loader
```

### Setup Instructions

1. Create virtual environment:
    
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # Linux/Mac
    .\myenv\Scripts\activate   # Windows
    ```
    
2. Install dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. Configure environment variables:
    
    ```bash
    cp .env.example .env
    # Edit .env with your configuration
    ```
    
4. Run data ingestion:
    
    ```bash
    python ingest.py
    ```
    
5. Start the application:
    ```bash
    python app.py
    ```