# Product Context

This file provides a high-level overview of the project and the expected product that will be created. Initially it is based upon projectBrief.md and all other available project-related information in the working directory. This file is intended to be updated as the project evolves, and should be used to inform all other modes of the project's goals and context.
2025-08-09 16:10:00 - Updated technologies to include quality improvement tools.

---

## Project Goal

* Create a tool to combine multiple text documents into a single file for easier management and processing

## Key Features

* Upload multiple individual files for combination
* Select an entire folder of documents to combine
* Filter files by extension when processing folders
* Sort files by name or modification date
* Support for multiple output formats (Markdown, JSON, YAML)
* Preprocessing options (remove extra empty lines, normalize line endings, remove trailing whitespace)
* Clean and intuitive user interface

## Target Users

* Developers needing to combine code snippets or documentation files
* Content managers working with multiple text documents
* Researchers compiling data from various sources
* Anyone who needs to merge multiple text files into a single document

## Technologies

* Python
* FastAPI (Backend API)
* Streamlit (Frontend UI)
* Pydantic (Data validation)
* Requests (HTTP client)
* uv (Dependency management)
* Ruff (Linting and formatting)
* mypy (Static type checking)
* pytest (Testing framework)
* pre-commit (Automated quality control)

## Main Challenges

* Ensuring robust file handling and error management
* Providing a seamless user experience for both file uploads and folder selection
* Maintaining backward compatibility when adding new features
* Handling various text encodings and file formats correctly
* Implementing and maintaining high code quality standards