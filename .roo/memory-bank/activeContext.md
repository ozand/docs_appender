# Active Context

This file tracks the project's current status, including recent changes, current goals, and open questions.
2025-08-09 16:05:00 - Updated context to include quality improvement focus.

## Current Focus

* Testing and verifying the new folder selection functionality
* Ensuring proper integration between frontend and backend for folder processing
* Validating extension filtering for folder processing

## Recent Changes

* Added folder selection capability to the application
* Implemented backend endpoint for processing folders with extension filtering
* Modified frontend UI to support both file uploads and folder selection
* Fixed backend import and startup issues
* Aligned backend and frontend ports to resolve connection issues
* Restructured backend to use `src/` directory layout
* Set up pre-commit hooks for automated quality control
* Developed comprehensive testing strategy with `pytest` for backend
* Organized auxiliary scripts in `scripts/development/` directory
* Performed regular code quality maintenance

## Open Questions/Issues

* Need to thoroughly test the new functionality with various folder structures and file types
* Should we add support for recursive folder processing?
* Are there any edge cases with extension filtering that need to be addressed?