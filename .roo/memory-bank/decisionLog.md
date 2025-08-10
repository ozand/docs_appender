# Decision Log

This file records architectural and implementation decisions using a list format.
2025-08-09 15:45:00 - Added decisions related to folder selection feature.

## Decision

* Implement a new endpoint `/combine-folder/` for processing folders
* Add UI elements in the frontend to allow users to choose between file uploads and folder selection
* Add extension filtering capability for folder processing

## Rationale 

* Extend the application functionality to handle folders in addition to individual files
* Provide users with more flexibility in how they combine documents
* Allow filtering by file extensions to give users control over which files are processed

## Implementation Details

* Created a new Pydantic model `CombineFolderRequest` for folder processing
* Implemented `/combine-folder/` endpoint in `backend/main.py` that accepts a folder path and extension filter
* Modified the frontend to include radio buttons for choosing input type (files or folder)
* Added a text input for folder path and extension pattern when folder selection is chosen
* Updated the frontend logic to send requests to the appropriate endpoint based on user selection
* Added validation for folder path existence and extension format