# Product Requirement Document (PRD): Space Station Academy App

## Core Objective
Transform the "Space Station Academy" educational project from local Jupyter Notebooks into a polished, immersive, and standalone local web application. The app will serve as an offline "time-capsule" deployed on a dedicated laptop for a 12-year-old student named Leonidas. It uses a narrative-driven sci-fi UI to teach Python programming and AI concepts, securely validating student submissions via WebAssembly, and providing Socratic guidance via a local LLM integration.

## Narrative Context
The student (Leonidas) is a Space Engineer aboard the damaged "Aether" Space Station. He must repair systems by writing Python code while interacting with a localized AI mentor (the Pi Agent) to outsmart a rogue Security AI (SEC-V4). Content will be displayed natively in Greek.

## Architecture: The WebAssembly-Hybrid Sandbox
*   **Target Environment:** A standalone, fully offline .deb application deployed on a dedicated Linux environment for the user leonidas.
*   **UI Shell:** HTML/CSS/JS web application with the Monaco Editor. Packaged as a native desktop window via PyWebView.
*   **Backend Server:** A lightweight Flask server. **Crucially, PyWebView will load http://localhost:PORT** (not file://) to ensure Web Workers and XHR function correctly. Flask will inject COOP and COEP security headers to enable SharedArrayBuffer.
*   **Code Execution (Frontend):** Student code executes in a **"Warm" Pyodide Web Worker** on the frontend. To prevent "phantom variables" without suffering cold-boot lag, each run executes in a fresh, isolated globals() dictionary. worker.terminate() is reserved strictly as a watchdog fallback for unbreakable infinite loops.
*   **Input Handling:** builtins.input is overridden. Pyodide pauses execution synchronously using SharedArrayBuffer and Atomics.wait while the UI thread captures user input.
*   **The Mock Bridge (Ollama/Tracker):** To bypass Wasm socket/disk restrictions, 'Mock' Python modules are injected into Pyodide. When the student calls ollama.chat() or tracker.update(), the mock translates this to a synchronous XMLHttpRequest out to the Flask Backend.
*   **The Backend Proxy:** The Flask server receives the mocked XHR requests, executes the native calls (hitting localhost:11434 for Ollama, or writing to disk), and returns the results. A threading.Lock() will synchronize all reads/writes to memory.txt.
*   **Pathing:** All hardcoded /home/justin/ paths are removed. The backend dynamically resolves paths.

## The Pi Agent Integration (Parallel Chat)
*   The Socratic Pi Agent chat is a dedicated UI panel.
*   It does **not** use Pyodide. The UI sends chat messages directly to the Flask backend via standard HTTP.
*   The Flask backend bundles the question, the student's current Monaco editor code (context), and the system prompts, queries the local Ollama service, and streams the response back to the UI using **Server-Sent Events (SSE)**.

## Validation (Anti-Cheat)
*   Full Abstract Syntax Tree (AST) parsing is implemented within the Pyodide environment to verify the structural integrity of the code (e.g., enforcing loops) before execution.
*   PyWebView's debug mode is set to False in production to disable DevTools, preventing students from bypassing the frontend AST checks.
