import re
import json
import yaml
from datetime import datetime
from typing import List, Optional, Dict, Any


def normalize_anchor(filename: str) -> str:
    """Генерирует валидную якорную ссылку для markdown из имени файла."""
    # Паттерн: разрешаем буквы, цифры, кириллицу, подчеркивание и дефис.
    # Дефис в конце [], чтобы он не интерпретировался как диапазон.
    allowed_chars_pattern = r'[^a-z0-9а-яё_\--]' 
    return re.sub(
        allowed_chars_pattern, '',
        filename.lower()
            .replace(' ', '-')
            .replace('.', '-')
            .replace('#', ''),
        flags=re.IGNORECASE
    ).strip('-')


def preprocess_content(content: str, options: Dict[str, bool]) -> str:
    """
    Выполняет предварительную обработку содержимого файла.
    
    Args:
        content (str): Исходное содержимое файла.
        options (Dict[str, bool]): Словарь с опциями обработки.
            Поддерживаемые ключи:
            - 'remove_extra_empty_lines': bool - Удалить лишние пустые строки (оставить максимум одну подряд).
            - 'normalize_line_endings': bool - Заменить все окончания строк на '\\n'.
            - 'remove_trailing_whitespace': bool - Удалить пробельные символы в конце строк.
            
    Returns:
        str: Обработанное содержимое.
    """
    if options.get('normalize_line_endings', False):
        # Заменяем CRLF и CR на LF
        content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    if options.get('remove_trailing_whitespace', False):
        # Разбиваем на строки, убираем пробелы в конце, соединяем обратно
        lines = content.split('\n')
        processed_lines = [line.rstrip() for line in lines]
        content = '\n'.join(processed_lines)
        
    if options.get('remove_extra_empty_lines', False):
        # Заменяем 3 и более пустых строки подряд на 2 пустых строки
        while '\n\n\n' in content:
            content = content.replace('\n\n\n', '\n\n')
        # Убираем пустые строки в самом начале
        content = content.lstrip('\n')
            
    return content


def combine_files_content(
    file_data_list: List[Dict[str, Any]], 
    sort_mode: str = 'name', 
    extensions: Optional[List[str]] = None,
    preprocessing_options: Optional[Dict[str, bool]] = None,
    output_format: str = 'markdown'
) -> str:
    """
    Объединяет содержимое файлов из списка словарей с данными файлов.
    
    Args:
        file_data_list: Список словарей, где каждый словарь содержит:
            - 'name': str - Имя файла.
            - 'content': str - Содержимое файла.
            - 'last_modified': datetime - Дата последнего изменения (или загрузки).
        sort_mode: Режим сортировки ('name', 'date_asc', 'date_desc').
        extensions: Список расширений для фильтрации (например, ['.txt', '.md']).
        preprocessing_options: Опции для предварительной обработки содержимого.
        output_format: Формат вывода ('markdown', 'json', 'yaml').

    Returns:
        str: Объединённое содержимое в выбранном формате.
    """
    if not file_data_list:
        empty_message = "No files found matching the criteria."
        if output_format == 'json':
            return json.dumps({"error": empty_message}, ensure_ascii=False, indent=2)
        elif output_format == 'yaml':
            return yaml.dump({"error": empty_message}, allow_unicode=True, default_flow_style=False)
        else: # markdown
            return "# Combined Files\n\nNo files found matching the criteria.\n"

    # --- 1. Фильтрация ---
    if extensions:
        filtered_files = [
            f for f in file_data_list 
            if any(f['name'].lower().endswith(ext) for ext in extensions)
        ]
    else:
        filtered_files = file_data_list

    if not filtered_files:
        empty_message = "No files found matching the criteria."
        if output_format == 'json':
            return json.dumps({"error": empty_message}, ensure_ascii=False, indent=2)
        elif output_format == 'yaml':
            return yaml.dump({"error": empty_message}, allow_unicode=True, default_flow_style=False)
        else: # markdown
            return "# Combined Files\n\nNo files found matching the criteria.\n"

    # --- 1.5. Предварительная обработка содержимого ---
    if preprocessing_options:
        for file_data in filtered_files:
            file_data['content'] = preprocess_content(file_data['content'], preprocessing_options)

    # --- 2. Сортировка ---
    if sort_mode == 'name':
        filtered_files.sort(key=lambda f: f['name'].lower())
    elif sort_mode == 'date_asc':
        filtered_files.sort(key=lambda f: f['last_modified'])
    elif sort_mode == 'date_desc':
        filtered_files.sort(key=lambda f: f['last_modified'], reverse=True)

    # --- 3. Создание контента в зависимости от формата ---
    if output_format.lower() == 'json':
        # Создаем структурированный JSON
        result = {
            "metadata": {
                "title": "Combined Files",
                "total_files": len(filtered_files),
                "sort_mode": sort_mode,
                "filter_extensions": extensions,
                "generated_at": datetime.now().isoformat()
            },
            "files": []
        }
        for file_data in filtered_files:
            result["files"].append({
                "name": file_data['name'],
                "last_modified": file_data['last_modified'].isoformat(),
                "content": file_data['content']
            })
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    elif output_format.lower() == 'yaml':
        # Создаем структурированный YAML
        result = {
            "metadata": {
                "title": "Combined Files",
                "total_files": len(filtered_files),
                "sort_mode": sort_mode,
                "filter_extensions": extensions,
                "generated_at": datetime.now().isoformat()
            },
            "files": []
        }
        for file_data in filtered_files:
            result["files"].append({
                "name": file_data['name'],
                "last_modified": file_data['last_modified'].isoformat(),
                "content": file_data['content']
            })
        return yaml.dump(result, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
    else: # markdown (по умолчанию)
        # Старая логика для Markdown
        all_content = ["# Combined Files\n\n## Table of Contents\n"]
        for i, file_data in enumerate(filtered_files, 1):
            anchor = normalize_anchor(file_data['name'])
            all_content.append(f"{i}. [{file_data['name']}](#{anchor})\n")
        all_content.append("\n---\n")

        for file_data in filtered_files:
            formatted_date = file_data['last_modified'].strftime('%Y-%m-%d %H:%M:%S')
            all_content.extend([
                f"\n---\n", 
                f"## {file_data['name']}\n", 
                f"*Last modified: {formatted_date}*\n\n",
                file_data['content'],
                f"\n\n---"
            ])

        # Убираем тройные и более переходы на новую строку
        combined_text = "".join(all_content)
        while '\n\n\n' in combined_text:
             combined_text = combined_text.replace('\n\n\n', '\n\n')
             
        return combined_text