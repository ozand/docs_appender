# Quality Improvement Plan

This file outlines the plan for improving the project's structure, maintainability, and adherence to best practices based on the established quality guidelines.

## 1. Project Structure & Organization (Align with `src/` layout)

* **Goal:** Restructure the backend and frontend directories to use a `src/` layout.
* **Actions:**
  * For the backend: Move the main application code (`main.py`, `shared/`) into a `src/backend/` directory. Update imports and configuration files (`Dockerfile`, `run_backend.bat`) accordingly.
  * For the frontend: Consider moving `app.py` into `src/frontend/` if it grows in complexity.
* **Rationale:** This aligns with the quality guideline's recommendation for a clear separation and mirroring of `src/` and `tests/` directories, improving modularity and clarity.
* **Status:** Completed for backend

## 2. Dependency Management & Environment Isolation

* **Goal:** Standardize dependency management using `uv` and ensure proper environment isolation.
* **Actions:**
  * In the backend: Create a `pyproject.toml` file. Use `uv add <package>` for runtime dependencies (e.g., `fastapi`, `uvicorn`, `pydantic`) and `uv add --dev <package>` for development dependencies (e.g., `pytest`, `ruff`, `mypy`). Ensure `.venv` is in `.gitignore`.
  * In the frontend: Create a `pyproject.toml` file. Use `uv add streamlit` and other necessary packages. Add dev dependencies as needed.
  * Consider using separate virtual environments for backend and frontend if they have conflicting dependencies or for better isolation (though `uv` handles this well).
* **Rationale:** Using `uv` and `pyproject.toml` provides a modern, efficient way to manage dependencies and environments, as recommended by the guidelines.
* **Status:** Completed - pyproject.toml files already exist and dependencies have been synced

## 3. Automated Quality Control (Pre-commit Hooks)

* **Goal:** Implement and configure pre-commit hooks for automated code quality checks.
* **Actions:**
  * Ensure a `.pre-commit-config.yaml` file exists in the root directory (it's already present).
  * Configure it to include:
    * `ruff` for linting and formatting (`ruff --fix`, `ruff-format`).
    * `mypy` for static type checking.
    * A custom hook for checking circular imports (if applicable).
  * Run `pre-commit install` to activate the hooks.
  * Ensure `.gitignore` excludes relevant files (logs, build artifacts, etc.).
* **Rationale:** This enforces code quality standards automatically, catching issues early in the development process.
* **Status:** Completed

## 4. Testing Strategy

* **Goal:** Develop a comprehensive testing strategy for both backend and frontend.
* **Actions:**
  * Backend:
    * Create a `tests/` directory mirroring the `src/` structure.
    * Write unit tests for the core logic in `shared/combine_logic.py`.
    * Write integration tests for the FastAPI endpoints in `main.py`.
    * Use `uv run pytest` to execute tests.
  * Frontend:
    * Consider using tools like `playwright` or `selenium` for end-to-end testing of the Streamlit UI, though this might be more complex.
    * For now, focus on backend tests.
  * Enforce test coverage using `pytest --cov=src --cov-report=xml`.
* **Rationale:** A robust testing suite ensures code correctness and makes refactoring safer.
* **Status:** Completed for backend

## 5. Scripts and Development Tooling (Follow `scripts/development/` structure)

* **Goal:** Organize any auxiliary scripts into a `scripts/development/` directory.
* **Actions:**
  * Create a `scripts/development/` directory in the project root.
  * Move or create any helper scripts (e.g., for code generation, refactoring, or maintenance tasks) in this directory.
  * Document each script's purpose and usage.
  * Consider archiving or deleting scripts that are no longer needed.
* **Rationale:** This keeps the core application code clean and separates auxiliary tasks, improving maintainability.
* **Status:** Completed

## 6. Code Quality & Refactoring

* **Goal:** Perform regular maintenance and refactoring tasks.
* **Actions:**
  * Use `ruff check . --select F401,F841 --fix` to remove unused imports and variables.
  * Regularly audit dependencies using `uv pip list --outdated`.
  * Follow the "small steps" rule for refactoring: make isolated changes, run tests, and commit.
* **Rationale:** This keeps the codebase clean, up-to-date, and easy to maintain.
* **Status:** Completed