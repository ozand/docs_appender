import tempfile
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel, validator
from shared.combine_logic import combine_files_content  # Импортируем логику из shared

app = FastAPI(title="File Combiner API", description="API for combining file contents.")

# --- Модели Pydantic для валидации ---


class CombineRequest(BaseModel):
    sort_mode: str = "name"
    extensions: Optional[List[str]] = None
    # Новые поля для расширенной обработки
    output_format: str = "markdown"
    remove_extra_empty_lines: bool = False
    normalize_line_endings: bool = False
    remove_trailing_whitespace: bool = False

    @validator("sort_mode")
    def sort_mode_must_be_valid(cls, v):
        if v not in ["name", "date_asc", "date_desc"]:
            raise ValueError("sort_mode must be one of 'name', 'date_asc', 'date_desc'")
        return v

    @validator("extensions")
    def extensions_must_start_with_dot(cls, v):
        if v:
            for ext in v:
                if not ext.startswith("."):
                    raise ValueError(
                        "Each extension must start with a dot (e.g., '.txt')"
                    )
        return v

    @validator("output_format")
    def output_format_must_be_valid(cls, v):
        if v.lower() not in ["markdown", "json", "yaml"]:
            raise ValueError("output_format must be one of 'markdown', 'json', 'yaml'")
        return v.lower()


# --- API Endpoints ---


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
    extensions: Optional[str] = Form(None),  # Принимаем как строку, потом парсим
    # Новые параметры из формы
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

    # Парсим extensions из строки
    extensions_list = None
    if extensions:
        extensions_list = [
            ext.strip().lower() for ext in extensions.split() if ext.strip()
        ]
        # Валидация расширений
        for ext in extensions_list:
            if not ext.startswith("."):
                raise HTTPException(
                    status_code=400, detail=f"Extension '{ext}' must start with a dot."
                )

    # Валидация sort_mode
    if sort_mode not in ["name", "date_asc", "date_desc"]:
        raise HTTPException(status_code=400, detail=f"Invalid sort_mode: {sort_mode}")

    # Валидация output_format
    output_format = output_format.lower()
    if output_format not in ["markdown", "json", "yaml"]:
        raise HTTPException(
            status_code=400, detail=f"Invalid output_format: {output_format}"
        )

    try:
        # Преобразуем UploadFile в формат, понятный нашей функции
        # tempfile.TemporaryDirectory используется для корректной очистки,
        # даже если переменная не используется напрямую.
        file_data_list = []
        with tempfile.TemporaryDirectory() as _tmpdirname:
            for file in files:
                # Читаем содержимое файла
                content = await file.read()
                # Декодируем из bytes в str (предполагаем UTF-8)
                try:
                    content_str = content.decode("utf-8")
                except UnicodeDecodeError:
                    # Если не UTF-8, используем замену символов
                    content_str = content.decode("utf-8", errors="replace")

                file_data_list.append(
                    {
                        "name": file.filename,
                        "content": content_str,
                        "last_modified": datetime.now(),  # Используем время загрузки как "дату модификации"
                    }
                )

        # Подготавливаем опции для предварительной обработки
        preprocessing_options = {
            "remove_extra_empty_lines": remove_extra_empty_lines,
            "normalize_line_endings": normalize_line_endings,
            "remove_trailing_whitespace": remove_trailing_whitespace,
        }

        # Вызываем логику объединения с новыми параметрами
        try:
            combined_content = combine_files_content(
                file_data_list,
                sort_mode,
                extensions_list,
                preprocessing_options,
                output_format,
            )
        except Exception as e:  # noqa: BLE001
            # Перехватываем любые ошибки из shared логики и превращаем их в HTTP 500
            raise HTTPException(
                status_code=500, detail=f"Error in combine logic: {str(e)}"
            ) from e

        # Определяем MIME-тип для ответа в зависимости от формата
        media_type_map = {
            "json": "application/json",
            "yaml": "application/yaml",
            "markdown": "text/markdown",
        }
        media_type = media_type_map.get(output_format, "text/plain")

        return PlainTextResponse(content=combined_content, media_type=media_type)

    except Exception as e:  # noqa: BLE001
        # Перехватываем любые другие непредвиденные ошибки
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        ) from e


if __name__ == "__main__":
    import uvicorn  # type: ignore[import-not-found] # noqa: F401

    uvicorn.run(app, host="0.0.0.0", port=8000)
