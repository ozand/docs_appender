import pytest
from datetime import datetime
from shared.combine_logic import combine_files_content, preprocess_content


def test_combine_files_content_basic():
    """Тест базового объединения файлов в формате Markdown."""
    file_data_list = [
        {
            'name': 'file1.txt',
            'content': 'Content of file 1.',
            'last_modified': datetime(2023, 10, 27, 10, 0, 0)
        },
        {
            'name': 'file2.txt',
            'content': 'Content of file 2.',
            'last_modified': datetime(2023, 10, 27, 11, 0, 0)
        }
    ]
    
    result = combine_files_content(file_data_list, sort_mode='name')
    
    # Проверяем, что результат содержит заголовки и содержимое файлов
    assert "# Combined Files" in result
    assert "## Table of Contents" in result
    assert "1. [file1.txt](#file1-txt)" in result
    assert "2. [file2.txt](#file2-txt)" in result
    assert "## file1.txt" in result
    assert "Content of file 1." in result
    assert "## file2.txt" in result
    assert "Content of file 2." in result


def test_combine_files_content_sort_by_date_asc():
    """Тест сортировки файлов по дате (возрастание)."""
    file_data_list = [
        {
            'name': 'z_file.txt',
            'content': 'Content Z.',
            'last_modified': datetime(2023, 10, 27, 12, 0, 0) # Позже
        },
        {
            'name': 'a_file.txt',
            'content': 'Content A.',
            'last_modified': datetime(2023, 10, 27, 10, 0, 0) # Раньше
        }
    ]
    
    result = combine_files_content(file_data_list, sort_mode='date_asc')
    
    # В режиме date_asc файл 'a_file.txt' должен быть первым
    lines = result.split('\n')
    # Найдем строку с первым файлом в оглавлении
    toc_start = lines.index("## Table of Contents") + 1
    first_toc_item = lines[toc_start].strip()
    assert first_toc_item == "1. [a_file.txt](#a_file-txt)"


def test_combine_files_content_filter_extensions():
    """Тест фильтрации файлов по расширениям."""
    file_data_list = [
        {
            'name': 'document.md',
            'content': '# Markdown Content',
            'last_modified': datetime(2023, 10, 27, 10, 0, 0)
        },
        {
            'name': 'script.py',
            'content': 'print("Hello")',
            'last_modified': datetime(2023, 10, 27, 11, 0, 0)
        },
        {
            'name': 'data.txt',
            'content': 'Plain text data',
            'last_modified': datetime(2023, 10, 27, 12, 0, 0)
        }
    ]
    
    # Фильтруем только .md и .txt файлы
    result = combine_files_content(file_data_list, extensions=['.md', '.txt'])
    
    assert "document.md" in result
    assert "data.txt" in result
    assert "script.py" not in result # .py файл должен быть отфильтрован


def test_combine_files_content_output_json():
    """Тест вывода в формате JSON."""
    import json
    
    file_data_list = [
        {
            'name': 'file1.txt',
            'content': 'Line 1\nLine 2',
            'last_modified': datetime(2023, 10, 27, 10, 0, 0)
        }
    ]
    
    result = combine_files_content(file_data_list, output_format='json')
    
    # Парсим JSON
    parsed_result = json.loads(result)
    
    assert parsed_result['metadata']['title'] == "Combined Files"
    assert len(parsed_result['files']) == 1
    assert parsed_result['files'][0]['name'] == 'file1.txt'
    assert parsed_result['files'][0]['content'] == 'Line 1\nLine 2'


def test_combine_files_content_output_yaml():
    """Тест вывода в формате YAML."""
    import yaml
    
    file_data_list = [
        {
            'name': 'file1.txt',
            'content': 'Line A\nLine B',
            'last_modified': datetime(2023, 10, 27, 10, 0, 0)
        }
    ]
    
    result = combine_files_content(file_data_list, output_format='yaml')
    
    # Парсим YAML
    parsed_result = yaml.safe_load(result)
    
    assert parsed_result['metadata']['title'] == "Combined Files"
    assert len(parsed_result['files']) == 1
    assert parsed_result['files'][0]['name'] == 'file1.txt'
    assert parsed_result['files'][0]['content'] == 'Line A\nLine B'


def test_combine_files_content_empty_list():
    """Тест с пустым списком файлов."""
    file_data_list = []
    
    result = combine_files_content(file_data_list)
    
    assert "No files found matching the criteria." in result


def test_preprocess_content_remove_extra_empty_lines():
    """Тест предварительной обработки: удаление лишних пустых строк."""
    content = "Line 1\n\n\n\nLine 2\n\n\nLine 3\n"
    options = {'remove_extra_empty_lines': True}
    
    result = preprocess_content(content, options)
    
    # Должно остаться максимум две пустые строки подряд
    assert "\n\n\n" not in result
    # И одна пустая строка в конце тоже должна быть удалена
    # Функция оставляет завершающий \n, если он был. Уточним тест.
    assert result == "Line 1\n\nLine 2\n\nLine 3\n"


def test_preprocess_content_normalize_line_endings():
    """Тест предварительной обработки: нормализация окончаний строк."""
    # Смешанные окончания строк: LF, CRLF, CR
    content = "Line 1\nLine 2\r\nLine 3\rLine 4"
    options = {'normalize_line_endings': True}
    
    result = preprocess_content(content, options)
    
    # Все должны быть заменены на LF (\n)
    expected = "Line 1\nLine 2\nLine 3\nLine 4"
    assert result == expected


def test_preprocess_content_remove_trailing_whitespace():
    """Тест предварительной обработки: удаление пробельных символов в конце строк."""
    content = "Line 1   \n  Line 2\t\nLine 3\n   "
    options = {'remove_trailing_whitespace': True}
    
    result = preprocess_content(content, options)
    
    expected = "Line 1\n  Line 2\nLine 3\n"
    assert result == expected


def test_preprocess_content_combined():
    """Тест комбинированной предварительной обработки."""
    content = "Line 1   \n\n  \n\n\nLine 2\t\r\nLine 3\r   \n   \n\n"
    options = {
        'remove_extra_empty_lines': True,
        'normalize_line_endings': True,
        'remove_trailing_whitespace': True
    }
    
    result = preprocess_content(content, options)
    
    expected = "Line 1\n\nLine 2\nLine 3\n\n"
    assert result == expected