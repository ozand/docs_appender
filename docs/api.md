# Документация API бэкенда

Бэкенд File Combiner App построен с помощью FastAPI и предоставляет REST API для объединения файлов.

**Базовый URL**: `http://localhost:8000/api/v1` (при локальном запуске)

**Интерактивная документация (Swagger UI)**: `http://localhost:8000/docs`

**Альтернативная документация (ReDoc)**: `http://localhost:8000/redoc`

---

## Эндпоинт: Объединить файлы

Объединяет загруженные файлы в один документ.

*   **URL**: `/combine`
*   **Метод**: `POST`
*   **Content-Type**: `multipart/form-data`

### Параметры запроса (FormData)

| Параметр | Тип | Обязательный | Описание |
| :--- | :--- | :--- | :--- |
| `files` | `file[]` | Да | Список файлов для объединения. |
| `sort_mode` | `string` | Нет (по умолчанию `name`) | Режим сортировки: `name`, `date_asc`, `date_desc`. |
| `extensions` | `string` | Нет | Список расширений, разделенных запятыми (например, `.txt,.md`). Если не указан, включаются все файлы. |
| `remove_extra_empty_lines` | `boolean` | Нет (по умолчанию `false`) | Удалить лишние пустые строки. |
| `normalize_line_endings` | `boolean` | Нет (по умолчанию `false`) | Нормализовать окончания строк. |
| `remove_trailing_whitespace` | `boolean` | Нет (по умолчанию `false`) | Удалить пробельные символы в конце строк. |
| `output_format` | `string` | Нет (по умолчанию `markdown`) | Формат вывода: `markdown`, `json`, `yaml`. |

### Ответы

*   **Успех (200 OK)**:
    *   **Content-Type**: `text/markdown`, `application/json` или `application/yaml` (в зависимости от `output_format`).
    *   **Тело**: Объединённый документ в указанном формате.

*   **Ошибка валидации (422 Unprocessable Entity)**:
    *   Не предоставлены обязательные параметры или параметры имеют неверный формат.
    *   **Content-Type**: `application/json`.
    *   **Тело**: Описание ошибки валидации.

*   **Внутренняя ошибка сервера (500 Internal Server Error)**:
    *   Произошла ошибка во время обработки запроса.
    *   **Content-Type**: `application/json`.
    *   **Тело**: Сообщение об ошибке.

---

## Эндпоинт: Скачать объединённый файл

Объединяет файлы и возвращает результат как прикреплённый файл для скачивания.

*   **URL**: `/download`
*   **Метод**: `POST`
*   **Content-Type**: `multipart/form-data`

### Параметры запроса (FormData)

Те же, что и у `/combine`.

### Ответы

*   **Успех (200 OK)**:
    *   **Content-Type**: `text/markdown`, `application/json` или `application/yaml`.
    *   **Content-Disposition**: `attachment; filename="..."`.
    *   **Тело**: Объединённый документ в указанном формате.

*   **Ошибки**: Те же, что и у `/combine`.