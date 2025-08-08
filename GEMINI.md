# Project Context for AI Assistant (GEMINI.md)

## Project Overview

This directory contains the "File Combiner App", a web application built with Python. Its primary function is to merge the contents of multiple text files into a single Markdown document. The application follows a client-server architecture, separating the backend logic from the user interface.

*   **Backend:** A RESTful API implemented using the FastAPI framework (`backend/main.py`). It handles file uploads, processes them according to user-defined parameters (sorting, filtering), and performs the core logic of combining file contents. The core logic is encapsulated in a shared module (`shared/combine_logic.py`).
*   **Frontend:** A user-friendly web interface built with Streamlit (`frontend/app.py`). It allows users to upload files, set options like sorting order and file extension filters, trigger the combination process, and view or download the resulting Markdown file.
*   **Shared Logic:** The core file combination logic resides in `shared/combine_logic.py` to promote code reuse between the backend API and potentially other interfaces.
*   **Dependency Management:** Dependencies for the backend and frontend are managed separately using `pyproject.toml` files and the `uv` tool, replacing older `requirements.txt` files.
*   **Execution:** A convenient Windows batch script (`run_app.bat`) provides an interactive menu to start the backend, frontend, or both components easily.

## Code Project Details

### Technologies Used

*   **Language:** Python (>=3.8)
*   **Backend Framework:** FastAPI
*   **Frontend Framework:** Streamlit
*   **ASGI Server (for backend):** Uvicorn (managed by `uv run`)
*   **Package/Dependency Manager:** `uv`
*   **API Interaction (Frontend):** `requests`

### Project Structure

```
.
├── backend/
│   ├── main.py          # FastAPI application entry point and API endpoints
│   └── pyproject.toml   # Backend dependencies (FastAPI, Uvicorn, etc.)
├── frontend/
│   ├── app.py           # Streamlit application entry point and UI logic
│   └── pyproject.toml   # Frontend dependencies (Streamlit, requests)
├── shared/
│   └── combine_logic.py # Core logic for combining file contents
├── run_app.bat          # Interactive Windows script to run backend/frontend
├── run_backend.bat      # (Deprecated) Windows script to run backend
├── run_frontend.bat     # (Deprecated) Windows script to run frontend
├── README.md            # Project documentation and usage instructions
└── .gitignore           # Specifies files/directories to be ignored by Git
```

### Building and Running

The project uses `uv` for managing dependencies and running the application. `uv` automatically handles creating virtual environments.

**Prerequisites:**

*   [`uv`](https://github.com/astral-sh/uv) must be installed.

**Installation:**

Dependencies are defined in `backend/pyproject.toml` and `frontend/pyproject.toml`. They are typically installed automatically when running the application for the first time using `uv run`. Explicit installation can be done:

```bash
# Install backend dependencies
cd backend
uv sync
cd ..

# Install frontend dependencies
cd frontend
uv sync
cd ..
```

**Running the Application:**

There are two main ways to run the application:

1.  **Using the Interactive Script (Windows):**
    *   Execute `run_app.bat`. This opens a menu allowing you to start the backend, frontend, or both.

2.  **Manual Execution with `uv run`:**
    *   **Backend:**
        ```bash
        cd backend
        # Starts the FastAPI server with auto-reload on code changes
        uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
        ```
        The backend API will be available at `http://localhost:8000`. Swagger UI documentation is at `http://localhost:8000/docs`.
    *   **Frontend:**
        ```bash
        cd frontend
        # Starts the Streamlit app
        uv run streamlit run app.py
        ```
        Streamlit will automatically open the application in your default web browser (usually at `http://localhost:8501`).

**Important:** The backend must be running for the frontend to function correctly, as the frontend sends requests to the backend API.

### Development Conventions

*   **Dependency Management:** Uses `pyproject.toml` with `uv` for fast and reliable dependency resolution and environment management. Separate `pyproject.toml` files for backend and frontend allow for independent dependency trees.
*   **API Design:** The backend is structured as a FastAPI application with clearly defined endpoints (`/`, `/combine/`) and uses Pydantic models (`CombineRequest`) for request validation.
*   **Shared Logic:** Core business logic (`combine_files_content`) is isolated in the `shared` module to ensure it can be easily tested and reused.
*   **Frontend Communication:** The Streamlit frontend communicates with the FastAPI backend exclusively via HTTP requests using the `requests` library.
*   **Entry Points:** The main entry points for execution are `backend/main.py` (for the API) and `frontend/app.py` (for the UI).