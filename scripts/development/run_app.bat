@echo off
setlocal

cd /d "%~dp0"

:menu
cls
echo ========================================
echo   File Combiner App - Launch Menu
echo ========================================
echo 1. Start Backend (FastAPI)
echo 2. Start Frontend (Streamlit - CLI)
echo 3. Start Frontend (Streamlit - Browser)
echo 4. Start both Backend and Frontend (in separate windows)
echo 5. Smart Start (Setup environment and run)
echo 6. Exit
echo ========================================
set /p choice=Enter the menu item number and press Enter: 

if "%choice%"=="1" goto start_backend
if "%choice%"=="2" goto start_frontend_cli
if "%choice%"=="3" goto start_frontend_browser
if "%choice%"=="4" goto start_both
if "%choice%"=="5" goto smart_start
if "%choice%"=="6" goto exit
echo.
echo Invalid choice. Please enter a number from 1 to 6.
timeout /t 2 >nul
goto menu

:start_backend
echo Starting FastAPI backend...
cd backend
REM Set PYTHONPATH to include the project root so 'shared' can be imported
set PYTHONPATH=%CD%\..
REM Run uv run from the backend directory to use its local venv and pyproject.toml
start "FastAPI Backend" /D "%CD%" cmd /k "uv run uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000"
cd ..
echo FastAPI backend started in a new window. (http://localhost:8000)
timeout /t 2 >nul
goto menu

:start_frontend_cli
echo Starting Streamlit frontend (in this window)...
cd frontend
uv run streamlit run app.py
cd ..
goto menu

:start_frontend_browser
echo Starting Streamlit frontend (opening in browser)...
cd frontend
start "Streamlit Frontend" /D "%CD%" cmd /k "uv run streamlit run app.py --server.headless false"
cd ..
timeout /t 2 >nul
goto menu

:start_both
echo Starting Backend and Frontend simultaneously...
call :start_backend_nopause
call :start_frontend_browser_nopause
goto menu

:start_backend_nopause
cd backend
REM Set PYTHONPATH to include the project root so 'shared' can be imported
set PYTHONPATH=%CD%\..
REM Run uv run from the backend directory to use its local venv and pyproject.toml
start "FastAPI Backend" /D "%CD%" cmd /k "uv run uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000"
cd ..
exit /b

:start_frontend_browser_nopause
cd frontend
start "Streamlit Frontend" /D "%CD%" cmd /k "uv run streamlit run app.py --server.headless false"
cd ..
exit /b

:smart_start
echo Starting Smart Start...
cd ..
uv run scripts/development/smart_start.py
cd scripts/development
goto menu

:exit
echo Goodbye!
timeout /t 1 >nul
exit /b