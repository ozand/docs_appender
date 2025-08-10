# Project Help Guide

This document provides an overview of the project structure, development workflow, and available scripts.

## Project Structure

```
Docs Appender/
├── backend/
│   ├── src/
│   │   ├── backend/
│   │   │   ├── __init__.py
│   │   │   └── main.py          # FastAPI application
│   │   ├── shared/
│   │   │   ├── __init__.py
│   │   │   └── combine_logic.py # Core logic for combining files
│   │   └── __init__.py
│   ├── pyproject.toml            # Backend dependencies
│   ├── uv.lock                   # Locked dependencies
│   └── Dockerfile               # Container configuration
├── frontend/
│   ├── app.py                   # Streamlit application
│   ├── pyproject.toml           # Frontend dependencies
│   └── uv.lock                  # Locked dependencies
├── tests/
│   ├── backend/
│   │   ├── __init__.py
│   │   └── test_main.py         # Tests for FastAPI endpoints
│   ├── shared/
│   │   ├── __init__.py
│   │   └── test_combine_logic.py # Tests for core logic
│   └── __init__.py
├── scripts/
│   └── development/
│       ├── README.md            # Documentation for scripts
│       ├── run_app.bat          # Run both services (Windows)
│       ├── run_app.sh           # Run both services (Unix/Linux/macOS)
│       ├── run_backend.bat      # Run backend service (Windows)
│       ├── run_frontend.bat     # Run frontend service (Windows)
│       ├── run_tests.bat        # Run tests (Windows)
│       └── run_tests.sh         # Run tests (Unix/Linux/macOS)
├── docs/                        # Documentation files
├── .gitignore                   # Git ignore patterns
├── .pre-commit-config.yaml      # Pre-commit hooks configuration
└── README.md                    # Project overview
```

## Development Workflow

### 1. Setting Up the Environment

1. Install `uv` for dependency management:
   ```bash
   pip install uv
   ```

2. Install dependencies for backend and frontend:
   ```bash
   cd backend
   uv sync
   cd ../frontend
   uv sync
   ```

### 2. Running the Application

#### Using Development Scripts

From the project root directory:

**Windows:**
```cmd
scripts\\development\\run_app.bat
```

**Unix/Linux/macOS:**
```bash
./scripts/development/run_app.sh
```

#### Manual Execution

1. Start the backend service:
   ```bash
   cd backend
   uv run uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start the frontend service:
   ```bash
   cd frontend
   uv run streamlit run app.py --server.port 8501
   ```

### 3. Running Tests

#### Using Development Scripts

**Windows:**
```cmd
scripts\\development\\run_tests.bat
```

**Unix/Linux/macOS:**
```bash
./scripts/development/run_tests.sh
```

#### Manual Execution

```bash
uv run pytest tests/ -v
```

### 4. Code Quality

The project uses several tools to ensure code quality:

1. **Pre-commit Hooks**: Automatically run on each commit
   - `ruff`: Linting and formatting
   - `mypy`: Static type checking

2. **Manual Quality Checks**:
   ```bash
   # Run ruff checks
   ruff check .
   
   # Run ruff formatting
   ruff format .
   
   # Run mypy type checking
   mypy backend/src frontend
   ```

## API Endpoints

### Backend (FastAPI)

1. `GET /` - Root endpoint with API information
2. `POST /combine/` - Combine uploaded files
3. `POST /combine-folder/` - Combine files from a specified folder

## Key Features

1. **File Combination**: Upload multiple files and combine their contents
2. **Folder Processing**: Select an entire folder to combine its contents
3. **Extension Filtering**: Filter files by extension when processing folders
4. **Sorting Options**: Sort files by name or modification date
5. **Multiple Output Formats**: Support for Markdown, JSON, and YAML
6. **Preprocessing Options**: 
   - Remove extra empty lines
   - Normalize line endings
   - Remove trailing whitespace

## Technologies Used

- **Backend**: FastAPI, Pydantic, uvicorn
- **Frontend**: Streamlit
- **Dependency Management**: uv
- **Code Quality**: ruff, mypy, pre-commit
- **Testing**: pytest
- **Containerization**: Docker

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all tests pass
5. Commit your changes using the pre-commit hooks
6. Push to the branch
7. Create a pull request