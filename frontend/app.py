import streamlit as st
import requests
import os
from io import BytesIO

# --- Конфигурация ---
# Получаем URL бэкенда из переменной окружения, по умолчанию локальный
BACKEND_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_URL = f"{BACKEND_BASE_URL}/combine/"

# --- Streamlit App ---
st.set_page_config(page_title="Объединятор Файлов", layout="wide")
st.title("🛠 Объединятор Файлов (Streamlit + FastAPI)")

# --- Виджеты ввода ---
st.header("1. Загрузите файлы")
uploaded_files = st.file_uploader("Выберите файлы", accept_multiple_files=True, type=["txt", "md", "py", "js", "html", "csv"]) # Можно указать нужные типы

# --- Отображение информации о загруженных файлах ---
if uploaded_files:
    total_size_bytes = 0
    total_lines = 0
    for file in uploaded_files:
        # Размер файла
        total_size_bytes += file.size
        # Количество строк (для текстовых файлов)
        # Нужно быть осторожным, так как file.read() перемещает указатель
        # Лучше использовать file.getvalue() если это BytesIO, или читать заново
        # Streamlit UploadedFile ведет себя как BytesIO
        file.seek(0) # Перемещаем указатель в начало
        try:
            # Декодируем содержимое для подсчета строк
            content = file.read().decode('utf-8')
            lines = content.count('\n')
            # Если файл не заканчивается на \n, добавляем 1 строку
            if content and not content.endswith('\n'):
                lines += 1
            total_lines += lines
        except UnicodeDecodeError:
            # Если файл не текстовый, пропускаем подсчет строк
            st.warning(f"Не удалось подсчитать строки в файле '{file.name}' (возможно, он не текстовый).")
        finally:
            file.seek(0) # Возвращаем указатель в начало после чтения
    
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
    st.markdown(f"**Информация о файлах:**")
    st.markdown(f"- **Количество файлов:** {len(uploaded_files)}")
    st.markdown(f"- **Общий размер:** {formatted_size} ({total_size_bytes} bytes)")
    st.markdown(f"- **Количество строк (в текстовых файлах):** ~{total_lines}")

st.header("2. Настройте параметры")
sort_mode = st.selectbox(
    "Сортировка файлов:",
    options=["name", "date_asc", "date_desc"],
    format_func=lambda x: {
        "name": "По имени файла (A-Z)",
        "date_asc": "По дате изменения (сначала старые)",
        "date_desc": "По дате изменения (сначала новые)"
    }[x],
    index=0 # По умолчанию 'name'
)

extensions_input = st.text_input(
    "Фильтр по расширениям (например: .txt .md .py):",
    placeholder="Оставьте пустым для всех файлов",
    help="Введите расширения файлов, разделенные пробелами."
)

# --- Кнопка действия ---
st.header("3. Объединить")
if st.button("🚀 Объединить файлы", type="primary"):
    if not uploaded_files:
        st.warning("Пожалуйста, загрузите хотя бы один файл.")
    else:
        with st.spinner("Объединяем файлы..."):
            try:
                # Подготовка данных для запроса
                files_data = [("files", (file.name, file, file.type)) for file in uploaded_files]
                
                # Подготовка данных формы
                data = {
                    "sort_mode": sort_mode
                }
                if extensions_input.strip():
                    data["extensions"] = extensions_input.strip()

                # Отправка POST запроса
                response = requests.post(API_URL, files=files_data, data=data)

                # Обработка ответа
                if response.status_code == 200:
                    combined_content = response.text
                    st.success(f"✅ Успешно объединено {len(uploaded_files)} файлов!")
                    
                    st.header("4. Результат")
                    # Результат не отображается в основном окне, только кнопка для скачивания
                    st.info("Объединение выполнено. Используйте кнопку ниже для скачивания результата.")
                    
                    # Кнопка для скачивания
                    st.download_button(
                        label="💾 Скачать результат (Markdown)",
                        data=combined_content,
                        file_name="combined_files.md",
                        mime="text/markdown"
                    )
                else:
                    st.error(f"Ошибка от API: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Ошибка сети при подключении к API: {e}")
            except Exception as e:
                st.error(f"Произошла непредвиденная ошибка: {e}")

# --- Информация ---
st.sidebar.title("ℹ️ О приложении")
st.sidebar.markdown("""
Это приложение позволяет объединять содержимое нескольких текстовых файлов в один документ Markdown.

**Как пользоваться:**
1. Загрузите файлы с помощью виджета.
2. Выберите способ сортировки.
3. При необходимости, укажите фильтр по расширениям.
4. Нажмите кнопку "Объединить файлы".
5. Просмотрите результат и при желании скачайте его.
""")