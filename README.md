Project Overview
Pair Program Prototype is a real-time collaborative coding web application featuring an AI-powered autocomplete system. It allows multiple users to join shared coding rooms where their edits synchronize instantly. The AI autocomplete helps users with coding suggestions based on context, boosting productivity. The frontend uses the Monaco code editor, while the backend is built with FastAPI and WebSocket for realtime communication.

How to Run Both Services
Backend (FastAPI)
Make sure Python 3.8+ is installed.

Navigate to the backend directory.

Install dependencies:

text
pip install -r requirements.txt
Run the backend server:

text
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
The backend serves the WebSocket connection and AI autocomplete API at localhost:8000.

Frontend (Static HTML + JS)
Open the index.html file in a browser or serve it via a static server (e.g., live-server, Python HTTP server).

The frontend connects to the backend WebSocket and autocomplete API on localhost.

You can open multiple tabs or browsers, create/join rooms, and collaboratively edit code with realtime syncing and AI autocomplete.

Architecture and Design Choices
Frontend: Uses Monaco Editor for a VS Code-like coding experience. Supports AI autocomplete via HTTP POST calls to backend autocomplete endpoint. WebSocket connection used for syncing code and room events.

Backend: FastAPI with ASGI WebSocket endpoints for real-time code syncing. Includes a simple AI autocomplete service (mocked) that provides context-aware suggestions.

Syncing Strategy: Last-write-wins approach; edits from any user are propagated after debounce. The frontend uses a flag to prevent recursion loops updating the editor from remote changes.

AI Autocomplete: Debounced 600ms after typing or manual Ctrl+Space trigger. Suggestion results are transformed and fed into Monaco's suggestion API dynamically.

Room Management: Simple room ID creation and joining mechanism for collaborative sessions.

What Would Be Improved Given More Time
Implement true Operational Transform (OT) or CRDT syncing for conflict-free real-time editing.

Replace mocked AI autocomplete with a true ML model API (e.g., OpenAI or Groq integrated).

Add user authentication and persistent session history.

Support multi-language detection and enhanced language server protocol (LSP) features.

Improve editor UI with themes, user cursors, and rich collaborative UX.

Add comprehensive error handling, logging, and scalability for backend.

Build a CI/CD pipeline for seamless deployment, and Dockerize both services.

Add unit and integration tests for backend and frontend.

Current Limitations
Syncing is last-write-wins which can cause occasional loss of edits if users type simultaneously.

AI autocomplete is mocked and provides only static keyword suggestions currently.

No authentication or user identity features exist.

Frontend and backend URLs must be manually configured for deployment scenarios.

Collaboration rooms have no persistence beyond WebSocket lifetime.

Only basic editor functionality is implemented; lacks advanced IDE features.