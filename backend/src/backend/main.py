"""
Main FastAPI application.

This module provides the main API for file combination functionality.
"""

import os
import tempfile
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
from shared.combine_logic import combine_files_content  # Импортируем логику из shared

app = FastAPI(title="File Combiner API", description="API for combining file contents.")


# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit default port
        "http://127.0.0.1:8501",  # Alternative localhost
        "http://localhost:3000",  # React default port
        "http://127.0.0.1:3000",  # Alternative React port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>File Combiner API</title>
        </head>
        <body>
            <h1>Welcome to the File Combiner API!</h1>
            <p>Use <code>/docs</code> to view the interactive Swagger documentation.</p>
            <p>Use <code>/redoc</code> to view the alternative ReDoc documentation.</p>
        </body>
    </html>
    """


@app.post("/combine/", response_class=PlainTextResponse)
async def combine_files_endpoint(
    files: List[UploadFile] = File(...),
    sort_mode: str = Form("name"),
    extensions: Optional[str] = Form(None),
    output_format: str = Form("markdown"),
    remove_extra_empty_lines: bool = Form(False),
    normalize_line_endings: bool = Form(False),
    remove_trailing_whitespace: bool = Form(False),
):
    """
    Combines uploaded files.

    - **files**: List of files to combine.
    - **sort_mode**: Sorting mode ('name', 'date_asc', 'date_desc').
    - **extensions**: String with space-separated extensions (e.g., ".txt .md").
    - **output_format**: Output format ('markdown', 'json', 'yaml').
    - **remove_extra_empty_lines**: Remove extra empty lines.
    - **normalize_line_endings**: Normalize line endings to LF (
    ).
    - **remove_trailing_whitespace**: Remove trailing whitespace from lines.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    # Parse extensions from string
    extensions_list = None
    if extensions:
        extensions_list = [
            ext.strip().lower() for ext in extensions.split() if ext.strip()
        ]
        # Validate extensions
        for ext in extensions_list:
            if not ext.startswith("."):
                raise HTTPException(
                    status_code=400, detail=f"Extension '{ext}' must start with a dot."
                )

    # Validate sort_mode
    if sort_mode not in ["name", "date_asc", "date_desc"]:
        raise HTTPException(status_code=400, detail=f"Invalid sort_mode: {sort_mode}")

    # Validate output_format
    output_format = output_format.lower()
    if output_format not in ["markdown", "json", "yaml"]:
        raise HTTPException(
            status_code=400, detail=f"Invalid output_format: {output_format}"
        )

    try:
        # Convert UploadFile to format expected by our function
        file_data_list = []
        with tempfile.TemporaryDirectory() as _tmpdirname:
            for file in files:
                # Read file content
                content = await file.read()
                # Decode from bytes to str (assuming UTF-8)
                try:
                    content_str = content.decode("utf-8")
                except UnicodeDecodeError:
                    # If not UTF-8, use replacement characters
                    content_str = content.decode("utf-8", errors="replace")

                file_data_list.append(
                    {
                        "name": file.filename,
                        "content": content_str,
                        "last_modified": datetime.now(),  # Use upload time as "modified time"
                    }
                )

        # Prepare preprocessing options
        preprocessing_options = {
            "remove_extra_empty_lines": remove_extra_empty_lines,
            "normalize_line_endings": normalize_line_endings,
            "remove_trailing_whitespace": remove_trailing_whitespace,
        }

        # Call combine logic with new parameters
        try:
            combined_content = combine_files_content(
                file_data_list,
                sort_mode,
                extensions_list,
                preprocessing_options,
                output_format,
            )
        except ValueError as e:
            # Handle specific validation errors from combine logic
            raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}") from e
        except OSError as e:
            # Handle file system errors
            raise HTTPException(
                status_code=500, detail=f"File system error: {str(e)}"
            ) from e
        except Exception as e:
            # Catch any other unexpected errors from combine logic
            raise HTTPException(
                status_code=500, detail=f"Error in combine logic: {str(e)}"
            ) from e

        # Determine MIME type based on format
        media_type_map = {
            "json": "application/json",
            "yaml": "application/yaml",
            "markdown": "text/markdown",
        }
        media_type = media_type_map.get(output_format, "text/plain")

        return PlainTextResponse(content=combined_content, media_type=media_type)

    except (ValueError, TypeError) as e:
        # Handle validation and type errors
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}") from e
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        ) from e


@app.post("/combine-folder/", response_class=PlainTextResponse)
async def combine_folder_endpoint(
    folder_path: str = Form(...),
    sort_mode: str = Form("name"),
    extensions: Optional[str] = Form(None),
    output_format: str = Form("markdown"),
    remove_extra_empty_lines: bool = Form(False),
    normalize_line_endings: bool = Form(False),
    remove_trailing_whitespace: bool = Form(False),
    max_depth: int = Form(0),  # 0 means unlimited depth
):
    """
    Combines files from a specified folder.

    - **folder_path**: Path to the folder containing files to combine.
    - **sort_mode**: Sorting mode ('name', 'date_asc', 'date_desc').
    - **extensions**: String with space-separated extensions (e.g., ".txt .md").
    - **output_format**: Output format ('markdown', 'json', 'yaml').
    - **remove_extra_empty_lines**: Remove extra empty lines.
    - **normalize_line_endings**: Normalize line endings to LF (
    ).
    - **remove_trailing_whitespace**: Remove trailing whitespace from lines.
    - **max_depth**: Maximum folder depth to process (0 for unlimited).
    """
    # Validate folder_path
    if not os.path.isdir(folder_path):
        raise HTTPException(
            status_code=400,
            detail=f"Folder path '{folder_path}' does not exist or is not a directory.",
        )

    # Validate max_depth
    if max_depth < 0:
        raise HTTPException(
            status_code=400,
            detail="max_depth must be a non-negative integer (0 for unlimited depth)",
        )

    # Parse extensions from string
    extensions_list = None
    if extensions:
        extensions_list = [
            ext.strip().lower() for ext in extensions.split() if ext.strip()
        ]
        # Validate extensions
        for ext in extensions_list:
            if not ext.startswith("."):
                raise HTTPException(
                    status_code=400, detail=f"Extension '{ext}' must start with a dot."
                )

    # Validate sort_mode
    if sort_mode not in ["name", "date_asc", "date_desc"]:
        raise HTTPException(status_code=400, detail=f"Invalid sort_mode: {sort_mode}")

    # Validate output_format
    output_format = output_format.lower()
    if output_format not in ["markdown", "json", "yaml"]:
        raise HTTPException(
            status_code=400, detail=f"Invalid output_format: {output_format}"
        )

    try:
        # Read files from folder recursively with depth limit
        file_data_list = []

        # Function for recursive directory scanning
        def scan_directory(current_path, current_depth, relative_root):
            # Stop recursion if max_depth is set and reached
            if max_depth > 0 and current_depth > max_depth:
                return

            try:
                for entry in os.scandir(current_path):
                    # Get relative path from root folder
                    relative_path = (
                        os.path.relpath(entry.path, relative_root)
                        if relative_root
                        else entry.name
                    )

                    if entry.is_file():
                        # Filter by extensions if specified
                        if extensions_list:
                            if any(
                                entry.name.lower().endswith(ext)
                                for ext in extensions_list
                            ):
                                pass  # File matches filter
                            else:
                                continue  # Skip file

                        # Read file content
                        try:
                            with open(entry.path, encoding="utf-8") as f:
                                content_str = f.read()
                        except UnicodeDecodeError:
                            # Use replacement for non-UTF-8 files
                            with open(
                                entry.path, encoding="utf-8", errors="replace"
                            ) as f:
                                content_str = f.read()

                        # Get file modification time
                        last_modified_timestamp = os.path.getmtime(entry.path)
                        last_modified_datetime = datetime.fromtimestamp(
                            last_modified_timestamp
                        )

                        # Create more descriptive filename with path
                        file_name_with_path = (
                            relative_path if current_depth > 0 else entry.name
                        )

                        file_data_list.append(
                            {
                                "name": file_name_with_path,
                                "content": content_str,
                                "last_modified": last_modified_datetime,
                                "relative_path": relative_path,  # Add relative path for JSON
                            }
                        )
                    elif entry.is_dir():
                        # Recursively process subdirectories
                        scan_directory(entry.path, current_depth + 1, relative_root)
            except PermissionError:
                # Skip directories we can't access
                pass

        # Start scanning from root folder
        scan_directory(folder_path, 0, folder_path)

        # Prepare preprocessing options
        preprocessing_options = {
            "remove_extra_empty_lines": remove_extra_empty_lines,
            "normalize_line_endings": normalize_line_endings,
            "remove_trailing_whitespace": remove_trailing_whitespace,
        }

        # Call combine logic with new parameters
        try:
            combined_content = combine_files_content(
                file_data_list,
                sort_mode,
                extensions_list,
                preprocessing_options,
                output_format,
            )
        except Exception as e:
            # Catch errors from shared logic
            raise HTTPException(
                status_code=500, detail=f"Error in combine logic: {str(e)}"
            ) from e

        # Determine MIME type based on format
        media_type_map = {
            "json": "application/yaml",
            "yaml": "application/yaml",
            "markdown": "text/markdown",
        }
        media_type = media_type_map.get(output_format, "text/plain")

        return PlainTextResponse(content=combined_content, media_type=media_type)

    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        ) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
