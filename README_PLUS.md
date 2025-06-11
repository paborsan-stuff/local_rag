# README_PLUS

## Overview
This document provides a summary and detailed instructions for running the application, from starting the Python (FastAPI) server to running the front-end in DesktopAssistant via npm.

## System Execution Flow
1. **Backend (Python Server)**
   - Start the server using `python api_server.py`. This server uses FastAPI to expose the `/api/ask` endpoint.
   - The endpoint in `api_server.py` receives requests from the UI, validates the prompt, and calls the `answer_query` function in `src/rag.py` to process and generate the response.
2. **User Interface (DesktopAssistant)**
   - The UI is located in the `DesktopAssistant` folder and runs using `npm run dev` through Vite.
   - The `PromptInput.jsx` component captures the user prompt and sends a POST request to the `/api/ask` endpoint.
   - The response from the backend is received in `OutputDisplay.jsx` and displayed in the chat box for the user.

## Instructions to Run the Application
1. **Run the Python Server:**
   - Ensure all Python dependencies are installed and the environment is properly configured.
   - From the project root, execute:
     ```bash
     python api_server.py
     ```
   - This will start the server at `http://localhost:8000`.

2. **Run the User Interface:**
   - Open a new terminal and navigate to the `DesktopAssistant` directory:
     ```bash
     cd DesktopAssistant && npm run dev
     ```
   - The application will start and can be viewed in the browser at `http://localhost:3000`.

## Additional Code Comments
- **api_server.py:**  
  - Defines the `/api/ask` endpoint that receives and processes the prompt from the UI, and calls `answer_query` in `src/rag.py` to handle the response logic.
- **src/rag.py:**  
  - Currently, the `answer_query` function is hardcoded to return "Testing", allowing easy verification of the connection between the UI and backend.
- **DesktopAssistant/src/components/PromptInput.jsx:**  
  - Captures the user input and sends a fetch request to `/api/ask`, passing the prompt to the backend.
- **DesktopAssistant/vite.config.js:**  
  - Configures a proxy that redirects requests with the `/api` prefix to `http://localhost:8000`, ensuring proper communication between the front-end and the Python server.

This document complements the main README and serves as a quick guide to understand the integration between system components and to test the complete connection from the Python server to the React interface.
