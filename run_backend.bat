@echo off
cd /d "%~dp0"
echo Starting FastAPI backend with uv...
cd backend
start "FastAPI Backend" /D "%CD%" cmd /k "uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo FastAPI backend started in a new window.
timeout /t 2 >nul