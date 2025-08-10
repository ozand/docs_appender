@echo off
cd /d "%~dp0"
echo Starting Streamlit frontend with uv...
cd frontend
start "Streamlit Frontend" /D "%CD%" cmd /k "uv run streamlit run app.py"
echo Streamlit frontend started in a new window.
timeout /t 2 >nul