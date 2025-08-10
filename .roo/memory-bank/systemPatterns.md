# System Patterns *Optional*

This file documents recurring patterns and standards used in the project.
It is optional, but recommended to be updated as the project evolves.
2025-08-09 15:50:00 - Added coding and architectural patterns.

## Coding Patterns

* Use of Pydantic models for request validation in FastAPI endpoints
* Implementation of try/except blocks for error handling
* Use of type hints for better code documentation and IDE support
* Separation of concerns by organizing code into backend, frontend, and shared modules

## Architectural Patterns

* Client-server architecture with FastAPI backend and Streamlit frontend
* RESTful API design with clearly defined endpoints
* Shared logic module (`shared/combine_logic.py`) for core functionality
* Environment-based configuration for API URLs

## Testing Patterns

* Manual testing with predefined test cases
* Use of test folders with various file types to validate functionality
* Regression testing to ensure existing features remain functional