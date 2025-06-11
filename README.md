Local RAG System API
This project outlines the development and deployment of an entirely local Retrieval Augmented Generation (RAG) system from scratch. The system is packaged as a FastAPI application for easy deployment. It's designed to be practical and inspired by real-life use cases.
The implementation utilizes a modular framework with four main components that can be easily swapped out: Text data, Embedding model, LLM (Large Language Model), and Vector store.
Project Setup
To set up and run the project, you will need the application code, the prepared data, the embedding model and tokenizer, the vector store, the document store, and the LLM.
To run the application, start the backend by executing:
  python api_server.py
Then, in a separate terminal, navigate to the DesktopAssistant directory and run:
  npm run dev

1.Prepare the Data:
The system is designed to handle a wide array of document types.
Initial data may be in formats like JSON, PDFs, emails, or Excel spreadsheets.
This data must be "normalized" by converting it into a string format.
The example uses synthetic product descriptions in JSON format and converts each SKU into its own text file.
You should have a directory with text files containing your product descriptions with the SKUs as the filenames.

2.Generate Document Store and Vector Store:
The process involves chunking the text data for efficient retrieval. The document_chunker function is used to split text into paragraphs, then words, creating chunks up to a specified token count (chunk_size), refining chunks based on punctuation if needed, and optionally applying overlap. Each final chunk is assigned a unique ID and structured with the text content and metadata, and a mapping is created where a unique document ID points to all the chunks within that document.
Next, the vector store is created by converting the text chunks into numerical representations called embeddings using an embeddings model. The example uses BAAI/bge-small-en-v1.5.
The tokenizer and the embeddings model must be saved locally.
An embedding is generated for each text chunk using the compute_embeddings function.
The create_vector_store function stores these chunk embeddings, mapped by their unique chunk IDs, organized by document IDs.
The vector store (initially a Python dictionary) is saved to a JSON file to persist. The document store (containing the chunks and metadata) is also saved to a JSON file.

The source suggests using a build notebook to generate these doc_store and vector_store files.
3. Download LLM:
An LLM is integrated to generate interactive responses.
The example uses a local Mistral-7B model with GGUF 3-bit quantization.
You need to download the LLM file (e.g., .gguf).

4 Organize Files for Deployment:
Set up a deployment directory containing the necessary files.
This directory should include: app.py (the Flask application code), Dockerfile, requirements.txt, the saved embeddings model files (model/embedding), the saved tokenizer files (model/tokenizer), the document store JSON (doc_store.json), the vector store JSON (vector_store.json), and the LLM file (e.g., mistral-7b-instruct-v0.2.Q3_K_L.gguf). The source provides an image of the directory structure.
Building and Running the Docker Container

The application is containerized using Docker.

1.Dockerfile: The Dockerfile sets up the environment, copies requirements, installs dependencies, copies the application code, and specifies the working directory as /app. It exposes port 5001 and sets the CMD to run app.py when the container launches. Note: Local paths in your application code (e.g., to models or data files) must be prefixed with /app because that is the working directory inside the container. Running the app in the container on a Mac may not access the GPU.
2.Build the Docker Image: Navigate to the deployment directory in your terminal and run the following command:
3.Replace <image-name> and <tag> with desired values (e.g., rag-api:latest).
4.Run the Docker Container: Once the image is built, run the container, mapping a local port (e.g., 5001) to the container's exposed port (5001):
5.Running the container automatically launches the Flask application inside it
