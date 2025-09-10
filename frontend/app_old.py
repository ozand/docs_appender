import os

import requests
import streamlit as st

# --- Конфигурация ---
# Получаем URL бэкенда из переменной окружения, по умолчанию локальный
BACKEND_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_URL_FILES = f"{BACKEND_BASE_URL}/combine/"
API_URL_FOLDER = f"{BACKEND_BASE_URL}/combine-folder/"

# --- Streamlit App ---
st.set_page_config(page_title="File Combiner", layout="wide")
st.title("🛠 File Combiner (Streamlit + FastAPI)")

# --- Виджеты ввода ---
st.header("1. Upload Files or Select Folder")

# Используем st.session_state для хранения выбора пользователя
if "input_type" not in st.session_state:
    st.session_state.input_type = "files"  # По умолчанию выбираем файлы

# Радио-кнопки для выбора типа ввода
input_type = st.radio(
    "Select input type:",
    ("Upload Files", "Select Folder"),
    index=0 if st.session_state.input_type == "files" else 1,
    horizontal=True,
)

# Обновляем session_state
if input_type == "Upload Files":
    st.session_state.input_type = "files"
else:
    st.session_state.input_type = "folder"

# Виджеты для загрузки файлов или выбора папки
uploaded_files = []
folder_path = ""
extensions_pattern = ""

if st.session_state.input_type == "files":
    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=["txt", "md", "py", "js", "html", "csv"],
    )  # Можно указать нужные типы
else:
    folder_path = st.text_input("Enter folder path:", key="folder_path_input")
    extensions_pattern = st.text_input(
        "Filter by extensions (e.g.: .txt .md .py):",
        placeholder="Leave empty for all files",
        help="Enter file extensions separated by spaces.",
        key="folder_extensions_input",
    )
    # Добавляем поле для ввода глубины обработки папок
    max_depth = st.number_input(
        "Folder depth (0 for unlimited):",
        min_value=0,
        value=0,
        help="Maximum folder depth to process (0 means unlimited depth)",
        key="folder_depth_input",
    )

# --- Отображение информации о загруженных файлах или выбранной папке ---
if st.session_state.input_type == "files" and uploaded_files:
    total_size_bytes = 0
    total_lines = 0
    for file in uploaded_files:
        # Размер файла
        total_size_bytes += file.size
        # Количество строк (для текстовых файлов)
        # Нужно быть осторожным, так как file.read() перемещает указатель
        # Лучше использовать file.getvalue() если это BytesIO, или читать заново
        # Streamlit UploadedFile ведет себя как BytesIO
        file.seek(0)  # Перемещаем указатель в начало
        try:
            # Декодируем содержимое для подсчета строк
            content = file.read().decode("utf-8")
            lines = content.count("\n")
            # Если файл не заканчивается на \n, добавляем 1 строку
            if content and not content.endswith("\n"):
                lines += 1
            total_lines += lines
        except UnicodeDecodeError:
            # Если файл не текстовый, пропускаем подсчет строк
            st.warning(
                f"Could not count lines in file '{file.name}' (it might be non-text)."
            )
        finally:
            file.seek(0)  # Возвращаем указатель в начало после чтения

    # Форматирование размера файла
    def format_file_size(size_bytes):
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024.0 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.2f} {size_names[i]}"

    formatted_size = format_file_size(total_size_bytes)

    # Отображение информации
    st.markdown("**File Info:**")
    st.markdown(f"- **Number of files:** {len(uploaded_files)}")
    st.markdown(f"- **Total size:** {formatted_size} ({total_size_bytes} bytes)")
    st.markdown(f"- **Line count (in text files):** ~{total_lines}")

elif st.session_state.input_type == "folder" and folder_path:
    import os

    try:
        if os.path.isdir(folder_path):
            # Подсчитываем количество файлов в папке (с учетом фильтра по расширениям, если задан)
            extensions_list = None
            if extensions_pattern.strip():
                extensions_list = [
                    ext.strip().lower()
                    for ext in extensions_pattern.split()
                    if ext.strip()
                ]

            file_count = 0
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    # Если задан фильтр по расширениям, проверяем соответствие
                    if extensions_list:
                        if any(filename.lower().endswith(ext) for ext in extensions_list):
                            file_count += 1
                    else:
                        file_count += 1

            st.markdown("**Folder Info:**")
            st.markdown(f"- **Folder path:** {folder_path}")
            st.markdown(f"- **Number of files (matching filter):** {file_count}")
        else:
            st.warning(f"Path '{folder_path}' is not a valid directory.")
    except Exception as e:
        st.error(f"Error accessing folder: {e}")

st.header("2. Configure Options")

# --- Основные параметры ---
sort_mode = st.selectbox(
    "File sorting:",
    options=["name", "date_asc", "date_desc"],
    format_func=lambda x: {
        "name": "By filename (A-Z)",
        "date_asc": "By modification date (oldest first)",
        "date_desc": "By modification date (newest first)",
    }[x],
    index=0,  # По умолчанию 'name'
)

extensions_input = st.text_input(
    "Filter by extensions (e.g.: .txt .md .py):",
    placeholder="Leave empty for all files",
    help="Enter file extensions separated by spaces.",
    key="options_extensions_input",
)

# --- Новые параметры для предварительной обработки и формата ---
st.subheader("Preprocessing Options")
col1, col2, col3 = st.columns(3)
with col1:
    remove_extra_empty_lines = st.checkbox("Remove extra empty lines", value=False)
with col2:
    normalize_line_endings = st.checkbox("Normalize line endings (to LF)", value=False)
with col3:
    remove_trailing_whitespace = st.checkbox("Remove trailing whitespace", value=False)

st.subheader("Output Format")
output_format = st.selectbox(
    "Select output format:",
    options=["markdown", "json", "yaml"],
    format_func=lambda x: x.upper(),
    index=0,  # По умолчанию Markdown
)

# --- Кнопка действия ---
st.header("3. Combine")
if st.button("🚀 Combine Files", type="primary"):
    if st.session_state.input_type == "files" and not uploaded_files:
        st.warning("Please upload at least one file.")
    elif st.session_state.input_type == "folder" and not folder_path:
        st.warning("Please enter a folder path.")
    else:
        with st.spinner("Combining files..."):
            try:
                if st.session_state.input_type == "files":
                    # Подготовка данных для запроса к endpoint'у файлов
                    files_data = [
                        ("files", (file.name, file, file.type)) for file in uploaded_files
                    ]

                    # Подготовка данных формы, включая новые параметры
                    data = {
                        "sort_mode": sort_mode,
                        "output_format": output_format,
                        "remove_extra_empty_lines": str(remove_extra_empty_lines).lower(),
                        "normalize_line_endings": str(normalize_line_endings).lower(),
                        "remove_trailing_whitespace": str(
                            remove_trailing_whitespace
                        ).lower(),
                    }
                    if extensions_input.strip():
                        data["extensions"] = extensions_input.strip()

                    # Отправка POST запроса
                    response = requests.post(API_URL_FILES, files=files_data, data=data)

                else:  # st.session_state.input_type == "folder"
                    # Подготовка данных для запроса к endpoint'у папки
                    files_data = []  # Для endpoint'а папки файлы не передаются

                    # Подготовка данных формы, включая новые параметры
                    data = {
                        "folder_path": folder_path,
                        "sort_mode": sort_mode,
                        "output_format": output_format,
                        "remove_extra_empty_lines": str(remove_extra_empty_lines).lower(),
                        "normalize_line_endings": str(normalize_line_endings).lower(),
                        "remove_trailing_whitespace": str(
                            remove_trailing_whitespace
                        ).lower(),
                        "max_depth": str(max_depth),  # Добавляем параметр глубины
                    }
                    if extensions_pattern.strip():
                        data["extensions"] = extensions_pattern.strip()

                    # Отправка POST запроса
                    response = requests.post(API_URL_FOLDER, files=files_data, data=data)

                # Обработка ответа
                if response.status_code == 200:
                    combined_content = response.text
                    if st.session_state.input_type == "files":
                        st.success(
                            f"✅ Successfully combined {len(uploaded_files)} files!"
                        )
                    else:
                        st.success(
                            f"✅ Successfully combined files from folder '{folder_path}'!"
                        )

                    st.header("4. Result")
                    # Результат не отображается в основном окне, только кнопка для скачивания
                    st.info(
                        "Combination completed. Use the button below to download the result."
                    )

                    # Определяем имя файла и MIME-тип для скачивания
                    mime_type_map = {
                        "json": "application/json",
                        "yaml": "application/yaml",
                        "markdown": "text/markdown",
                    }
                    file_extension_map = {
                        "json": ".json",
                        "yaml": ".yaml",
                        "markdown": ".md",
                    }

                    mime_type = mime_type_map.get(output_format, "text/plain")
                    file_extension = file_extension_map.get(output_format, ".txt")

                    # Кнопка для скачивания
                    st.download_button(
                        label=f"💾 Download Result ({output_format.upper()})",
                        data=combined_content,
                        file_name=f"combined_files{file_extension}",
                        mime=mime_type,
                    )
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Network error connecting to API: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# --- Информация ---
st.sidebar.title("ℹ️ About")
st.sidebar.markdown(
    """
This application allows you to combine the contents of multiple text files into a single document.

**How to use:**
1. Choose input type: upload files or select a folder.
2. If uploading files:
    - Use the file uploader widget.
3. If selecting a folder:
    - Enter the folder path.
    - (Optional) Specify a filter by extensions for the folder.
    - (Optional) Specify folder depth for recursive processing.
4. Choose the sorting method.
5. Configure preprocessing options and output format.
6. Click the "Combine Files" button.
7. Review the result and download it if desired.
"""
)
