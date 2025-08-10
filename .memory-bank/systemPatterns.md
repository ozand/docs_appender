# System Patterns

This file documents recurring patterns and standards used in the project.
It is optional, but recommended to be updated as the project evolves.

## Coding Patterns

* Use of Pydantic models for request validation in FastAPI endpoints
* Implementation of try/except blocks for error handling
* Use of type hints for better code documentation and IDE support
* Separation of concerns by organizing code into backend, frontend, and shared modules
* Comprehensive error handling with appropriate HTTP status codes
* Use of form data for API endpoints to handle file uploads
* Adding necessary dependencies to pyproject.toml when needed
* Creation of development scripts to automate common tasks
* Recursive directory traversal with depth control
* Optional field handling in data structures for backward compatibility

## Architectural Patterns

* Client-server architecture with FastAPI backend and Streamlit frontend
* RESTful API design with clearly defined endpoints
* Shared logic module (`shared/combine_logic.py`) for core functionality
* Environment-based configuration for API URLs
* Separation of source code and tests following src/ layout pattern
* Use of virtual environments for dependency isolation

## Testing Patterns

* Unit testing for core logic functions
* Integration testing for API endpoints
* Use of pytest for test execution
* Test organization mirroring source code structure
* Manual testing with predefined test cases
* Use of test folders with various file types to validate functionality
* Regression testing to ensure existing features remain functional
* Adding missing dependencies to fix test import errors
* Testing optional field handling in data structures

## Quality Control Patterns

* Automated code formatting with ruff
* Static type checking with mypy
* Pre-commit hooks for automated quality checks
* Regular code quality maintenance
* Dependency management with uv and pyproject.toml
* Development script organization in `scripts/development/` directory
* Creation of smart start scripts to streamline development workflow