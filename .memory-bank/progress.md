# Progress

This file tracks the project's progress using a task list format.

## Completed Tasks

* Added folder selection functionality to the backend API
* Implemented new endpoint `/combine-folder/` in `backend/src/backend/main.py` for processing folders
* Modified frontend UI to allow folder selection
* Added input field for file extension patterns when selecting a folder
* Updated frontend logic to handle both file uploads and folder selection
* Fixed backend import and startup issues
* Aligned backend and frontend ports to resolve connection issues
* Restructured backend to use `src/` directory layout
* Set up pre-commit hooks for automated quality control
* Developed comprehensive testing strategy with `pytest` for backend
* Organized auxiliary scripts in `scripts/development/` directory
* Performed regular code quality maintenance
* Added requests dependency to both backend and frontend pyproject.toml files
* Verified all tests pass (17/17)
* Verified all pre-commit hooks pass
* Created smart start scripts for simplified project setup and launch
* Updated run_app.bat to use correct import paths for FastAPI application
* Implemented recursive folder processing with depth control
* Added folder path information in JSON output for better structure visualization
* Updated frontend UI to include depth control for folder processing
* Added unit tests for recursive folder processing functionality
* Verified all tests pass (19/19) after implementing recursive folder processing

## Current Tasks

* None

## Next Steps

* Consider implementing additional features for folder processing
* Review and refactor code for any potential improvements