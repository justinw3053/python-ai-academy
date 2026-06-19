# Issues: Space Station Academy App

## Issue 1: Project Initialization & Flask Backend Foundation
*   **Description:** Set up the basic project structure and a multi-threaded Flask server that serves static files and provides a basic testing endpoint.
*   **Acceptance Criteria:**
    *   Python virtual environment is configured with Flask and pywebview.
    *   Directory structure is created (/backend, /frontend, /content).
    *   A main.py Flask server runs on localhost with threaded=True and serves an index.html file.
    *   Flask is configured to inject Cross-Origin-Opener-Policy: same-origin and Cross-Origin-Embedder-Policy: require-corp headers globally.

## Issue 2: PyWebView Desktop Shell Integration
*   **Description:** Wrap the Flask server in a native desktop window using PyWebView.
*   **Acceptance Criteria:**
    *   A launcher script starts the Flask server in a background thread.
    *   A socket/HTTP probe-wait loop verifies Flask is bound and running before opening the PyWebView window pointing to the local Flask URL.
    *   The PyWebView window is configured with debug=False.
    *   Closing the PyWebView window successfully terminates the Flask server.

## Issue 3: Content Engine & UI Skeleton
*   **Description:** Build the frontend HTML/CSS/JS shell, load Monaco, and build the backend parser for .ipynb files.
*   **Acceptance Criteria:**
    *   Backend JSON parser reads .ipynb files with encoding='utf-8' (for Greek).
    *   Parser splits code cells at # === AUTOMATED CHECK ===, holding assertions back from the UI.
    *   index.html has sci-fi styling with three panels: Narrative, Code Editor, and Terminal/Chat.
    *   The Monaco Editor is bundled locally and configured for Python syntax highlighting.

## Issue 4: Local Pyodide Web Worker & Code Execution
*   **Description:** Integrate offline Pyodide to run inside a Web Worker.
*   **Acceptance Criteria:**
    *   Pyodide binaries are vendored in Flask's static/ directory for 100% offline use.
    *   A Web Worker (worker.js) initializes Pyodide.
    *   Clicking Run executes the Monaco code + hidden assertions in a fresh, isolated globals() dictionary (Warm Worker strategy).
    *   sys.stdout is captured and streamed back to the UI Terminal panel.

## Issue 5: Synchronous input() Handling via SharedArrayBuffer
*   **Description:** Pause Pyodide execution when Python code calls input(), wait for UI input, and resume.
*   **Acceptance Criteria:**
    *   builtins.input is overridden inside the Pyodide environment.
    *   When input() is called, the worker sends a message to the UI to display an input prompt and blocks using Atomics.wait on a SharedArrayBuffer.
    *   User input in the UI is written to the SharedArrayBuffer and Atomics.notify unblocks Pyodide.

## Issue 6: AST Anti-Cheat Validation
*   **Description:** Implement the AST parser inside the Pyodide worker to validate code structure before execution.
*   **Acceptance Criteria:**
    *   A Python validation function validates the student's source code against required AST node types (e.g., ast.For).
    *   The worker runs this AST check before exec().
    *   If validation fails, execution aborts and an error message is returned to the UI.

## Issue 7: The Python 'Mock' Bridge (Tracker & Local File I/O)
*   **Description:** Implement mock modules in Pyodide that forward state-saving requests to the Flask backend via synchronous XHR.
*   **Acceptance Criteria:**
    *   Flask endpoint /api/track writes updates to dynamically resolved path (e.g., ~/.local/share/Space_Station_Academy/memory.txt) using threading.Lock.
    *   Mock tracker and ollama modules are injected into Pyodide's sys.modules.
    *   Mock calls trigger synchronous XHR to Flask endpoints.

## Issue 8: Pi Agent Socratic Chat & Ollama Integration (SSE)
*   **Description:** Build the parallel communication channel for the Socratic Tutor.
*   **Acceptance Criteria:**
    *   Flask endpoint /api/chat accepts a user message and context.
    *   Flask communicates with the local Ollama service (http://localhost:11434).
    *   Flask streams the LLM response to the frontend using Server-Sent Events (SSE).
    *   The UI displays the streaming response.

## Issue 9: Offline .deb Packaging & Systemd Integration
*   **Description:** Package the application as a .deb file with proper desktop integration.
*   **Acceptance Criteria:**
    *   A build script bundles the Python environment, Flask, PyWebView, and static assets.
    *   The .deb installs cleanly on Linux.
    *   Systemd manages headless backend services (if applicable), while PyWebView starts via a .desktop file.
