#!/bin/bash

# Получаем директорию, где находится скрипт
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Функция для отображения меню
show_menu() {
    clear
    echo "========================================"
    echo "  File Combiner App - Меню запуска"
    echo "========================================"
    echo "1. Запустить Backend (FastAPI)"
    echo "2. Запустить Frontend (Streamlit)"
    echo "3. Запустить и Backend, и Frontend"
    echo "4. Выйти"
    echo "========================================"
    read -p "Введите номер пункта меню и нажмите Enter: " choice
}

# Функция для запуска бэкенда
start_backend() {
    echo "Запуск FastAPI backend..."
    cd backend || exit
    # Используем nohup и & для запуска в фоне
    nohup uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
    BACKEND_PID=$!
    echo "FastAPI backend запущен в фоне (PID: $BACKEND_PID). Логи: backend.log"
    echo "Доступен по адресу: http://localhost:8000"
    cd ..
}

# Функция для запуска фронтенда
start_frontend() {
    echo "Запуск Streamlit frontend..."
    cd frontend || exit
    uv run streamlit run app.py
    cd ..
}

# Функция для запуска обоих
start_both() {
    start_backend
    # Небольшая пауза, чтобы бэкенд успел стартовать
    sleep 3
    # Запускаем фронтенд в новом терминале (если возможно)
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal --title="Streamlit Frontend" -- bash -c "cd '$SCRIPT_DIR/frontend' && echo 'Запуск Streamlit frontend...' && uv run streamlit run app.py; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -title "Streamlit Frontend" -e bash -c "cd '$SCRIPT_DIR/frontend' && echo 'Запуск Streamlit frontend...' && uv run streamlit run app.py; exec bash"
    else
        echo "Не найден терминал для автоматического запуска фронтенда. Пожалуйста, запустите 'cd frontend && uv run streamlit run app.py' вручную."
    fi
}

# Основной цикл
while true; do
    show_menu
    case $choice in
        1)
            start_backend
            read -p "Нажмите Enter, чтобы вернуться в меню..."
            ;;
        2)
            start_frontend
            ;;
        3)
            start_both
            read -p "Нажмите Enter, чтобы вернуться в меню..."
            ;;
        4)
            echo "До свидания!"
            exit 0
            ;;
        *)
            echo "Неверный выбор. Пожалуйста, введите число от 1 до 4."
            sleep 2
            ;;
    esac
done