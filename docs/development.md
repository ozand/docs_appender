# Руководство по разработке

Это руководство предназначено для разработчиков, которые хотят внести вклад в проект или понять его внутреннюю структуру.

## Структура проекта

```
.
├── backend/                 # Бэкенд FastAPI
│   ├── main.py              # Основной файл приложения
│   └── pyproject.toml       # Зависимости и метаданные
├── frontend/                # Фронтенд Streamlit
│   ├── app.py               # Основной файл приложения
│   └── pyproject.toml       # Зависимости и метаданные
├── shared/                  # Общая логика
│   └── combine_logic.py     # Функции объединения и обработки
├── tests/                   # Тесты
│   └── shared/
│       └── test_combine_logic.py
├── docs/                    # Документация
├── .github/workflows/       # GitHub Actions CI/CD
├── .pre-commit-config.yaml  # Конфигурация pre-commit
├── docker-compose.yml       # Конфигурация Docker Compose
├── run_app.bat / .sh        # Скрипты запуска
├── run_tests.bat / .sh      # Скрипты запуска тестов
└── README.md / docs/index.md # Документация
```

## Разработка с `uv`

Проект активно использует `uv` для управления зависимостями и виртуальными средами.

### Установка зависимостей для разработки

```bash
# Для бэкенда
cd backend
uv sync --dev
cd ..

# Для фронтенда
cd frontend
uv sync --dev
cd ..
```

### Запуск приложения в режиме разработки

```bash
# Бэкенд с авто-reload
cd backend
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
cd ..

# Фронтенд с авто-reload
cd frontend
uv run streamlit run app.py
cd ..
```

### pre-commit хуки

Проект использует `pre-commit` для обеспечения качества кода.

**Установка хуков**:
```bash
cd backend # или frontend
uv run pre-commit install
cd ..
```

**Ручной запуск хуков**:
```bash
cd backend
uv run pre-commit run --all-files
cd ..
```

Хуки включают:
*   `ruff check`: линтинг.
*   `ruff format`: форматирование.
*   `mypy`: статическая проверка типов.

## Тестирование

Проект использует `pytest` для написания и запуска тестов.

### Запуск тестов

```bash
cd backend # pytest установлен в окружении бэкенда
uv run pytest ../tests/shared -v
```

### Покрытие кода

```bash
cd backend
uv run pytest ../tests/shared --cov=../shared --cov-report=html
cd ..
# Отчет будет в htmlcov/
```

## CI/CD

Проект использует GitHub Actions для CI/CD.

**Файл конфигурации**: `.github/workflows/ci.yml`

**Задачи (jobs)**:
1.  `lint`: запуск `ruff check` и `ruff format --check`.
2.  `type-check`: запуск `mypy`.
3.  `test`: запуск `pytest`.

## Стиль кода

Проект следует рекомендациям `ruff`.

*   **Линтинг**: `ruff check`
*   **Форматирование**: `ruff format`

Конфигурация находится в `pyproject.toml` каждого компонента.

## Типизация

Проект использует `mypy` для статической проверки типов.

Конфигурация `mypy` находится в `pyproject.toml` каждого компонента.

## Документация

Документация написана в формате Markdown и хранится в директории `docs/`.