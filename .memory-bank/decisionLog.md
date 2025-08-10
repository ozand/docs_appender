# Decision Log

This file records architectural and implementation decisions using a list format.

## Decision

* Implement a new endpoint `/combine-folder/` for processing folders
* Add UI elements in the frontend to allow users to choose between file uploads and folder selection
* Add extension filtering capability for folder processing
* Add requests dependency to both backend and frontend pyproject.toml files
* Create smart start scripts to simplify project setup and execution
* Enhance folder processing with recursive scanning and depth control
* Add folder path information in JSON output for better structure visualization

## Rationale 

* Extend the application functionality to handle folders in addition to individual files
* Provide users with more flexibility in how they combine documents
* Allow filtering by file extensions to give users control over which files are processed
* Fix test import errors by adding the missing requests dependency
* Simplify the development workflow by automating environment setup and application launch
* Enable processing of nested folder structures to handle complex directory hierarchies
* Provide better visualization of folder structure in JSON output for easier navigation

## Implementation Details

* Created a new Pydantic model `CombineFolderRequest` for folder processing
* Implemented `/combine-folder/` endpoint in `backend/src/backend/main.py` that accepts a folder path and extension filter
* Modified the frontend to include radio buttons for choosing input type (files or folder)
* Added a text input for folder path and extension pattern when folder selection is chosen
* Updated the frontend logic to send requests to the appropriate endpoint based on user selection
* Added validation for folder path existence and extension format
* Added requests dependency to both backend and frontend pyproject.toml files
* Verified that all tests pass after adding the dependency
* Created `smart_start.bat` for Windows with options for normal startup and cleanup mode
* Created `smart_start.sh` for Unix/Linux/macOS systems
* Created `smart_start.py` Python script for cross-platform compatibility
* Updated `run_app.bat` to include an option to run the smart start script
* Updated `scripts/development/README.md` to document the new scripts
* Verified that virtual environments are created correctly and dependencies are installed
* Confirmed that both backend and frontend services can start successfully
* Enhanced folder scanning with recursive directory traversal and depth control parameter (0 = unlimited depth)
* Added relative path information to JSON output to show folder structure
* Updated frontend UI to include depth control input for folder processing
* Modified shared logic to handle relative paths in file data for better JSON structure visualization

## Quality Improvement Decisions

* Restructure backend code to use `src/` directory layout for better organization
* Implement automated quality control with pre-commit hooks (ruff, mypy)
* Organize development scripts in `scripts/development/` directory
* Develop comprehensive testing strategy with pytest for both unit and integration tests
* Standardize dependency management using `uv` and `pyproject.toml`
* Create smart start scripts to streamline development environment setup