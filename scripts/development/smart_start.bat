@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 > nul
echo.
echo [ROCKET] Smart Start for File Combiner App
echo --------------------------------------------------
echo.

REM Check for parameters
set CLEAR_MODE=false
set SHOW_HELP=false
set UNKNOWN_PARAM=false

if "%1"=="--clear" (
    set CLEAR_MODE=true
    echo [INFO] Cleanup mode activated
    echo.
) else if "%1"=="--help" (
    set SHOW_HELP=true
) else if not "%1"=="" (
    set UNKNOWN_PARAM=true
)

if "%SHOW_HELP%"=="true" (
    echo [HELP] Smart Start Usage:
    echo.
    echo   smart_start.bat          - Normal startup
    echo   smart_start.bat --clear  - Startup with full cleanup
    echo   smart_start.bat --help   - Show this help
    echo.
    echo [INFO] --clear mode cleans:
    echo   - __pycache__ directories and .pyc files
    echo   - All logs and temporary files
    echo   - uv cache directories
    echo   - Virtual environments (.venv directories)
    echo.
    pause
    exit /b 0
)

if "%UNKNOWN_PARAM%"=="true" (
    echo [ERROR] Unknown parameter: %1
    echo [HELP] Use: smart_start.bat --help
    pause
    exit /b 1
)

REM Check if Python is available
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python and add to PATH.
    pause
    exit /b 1
)

REM Check if uv is available
uv --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] uv not found. Install uv (https://github.com/astral-sh/uv) and add to PATH.
    pause
    exit /b 1
)

REM Change to project directory
cd /d "%~dp0..\.."

REM Perform cleanup if --clear mode is active
if "%CLEAR_MODE%"=="true" (
    echo [CLEANUP] Performing full cleanup...
    
    REM Clean __pycache__ directories
    echo [CLEANUP] Removing __pycache__ directories...
    for /r %%i in (__pycache__) do (
        if exist "%%i" (
            echo   Removing: %%i
            rmdir /s /q "%%i" > nul 2>&1
        )
    )
    
    REM Clean .pyc files
    echo [CLEANUP] Removing .pyc files...
    del /s /q *.pyc > nul 2>&1
    
    REM Clean logs
    echo [CLEANUP] Removing log files...
    del /q *.log > nul 2>&1
    
    REM Clean temporary files
    echo [CLEANUP] Removing temporary files...
    del /q temp_* > nul 2>&1
    del /q tmp_* > nul 2>&1
    
    REM Clean uv cache directories
    echo [CLEANUP] Removing uv cache directories...
    if exist "backend\.uv" (
        echo   Removing: backend\.uv
        rmdir /s /q "backend\.uv" > nul 2>&1
    )
    if exist "frontend\.uv" (
        echo   Removing: frontend\.uv
        rmdir /s /q "frontend\.uv" > nul 2>&1
    )
    if exist "scripts\development\.uv" (
        echo   Removing: scripts\development\.uv
        rmdir /s /q "scripts\development\.uv" > nul 2>&1
    )
    
    REM Clean virtual environments
    echo [CLEANUP] Removing virtual environments...
    if exist "backend\.venv" (
        echo   Removing: backend\.venv
        rmdir /s /q "backend\.venv" > nul 2>&1
    )
    if exist "frontend\.venv" (
        echo   Removing: frontend\.venv
        rmdir /s /q "frontend\.venv" > nul 2>&1
    )
    
    REM Clean test cache directories
    echo [CLEANUP] Removing test cache directories...
    if exist ".pytest_cache" (
        echo   Removing: .pytest_cache
        rmdir /s /q ".pytest_cache" > nul 2>&1
    )
    if exist ".mypy_cache" (
        echo   Removing: .mypy_cache
        rmdir /s /q ".mypy_cache" > nul 2>&1
    )
    if exist ".ruff_cache" (
        echo   Removing: .ruff_cache
        rmdir /s /q ".ruff_cache" > nul 2>&1
    )
    
    echo [SUCCESS] Cleanup completed!
    echo.
)

REM Create virtual environments and install dependencies
echo [SETUP] Setting up backend environment...
cd backend
echo [SETUP] Creating virtual environment for backend...
uv venv
if errorlevel 1 (
    echo [ERROR] Failed to create backend virtual environment
    cd ..
    pause
    exit /b 1
)

echo [SETUP] Installing backend dependencies...
uv sync
if errorlevel 1 (
    echo [ERROR] Failed to install backend dependencies
    cd ..
    pause
    exit /b 1
)
cd ..

echo [SETUP] Setting up frontend environment...
cd frontend
echo [SETUP] Creating virtual environment for frontend...
uv venv
if errorlevel 1 (
    echo [ERROR] Failed to create frontend virtual environment
    cd ..
    pause
    exit /b 1
)

echo [SETUP] Installing frontend dependencies...
uv sync
if errorlevel 1 (
    echo [ERROR] Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)
cd ..

REM Run the application
echo [START] Launching File Combiner App
echo.

REM Pass parameters to run_app.bat
if "%CLEAR_MODE%"=="true" (
    call scripts\development\run_app.bat
) else (
    call scripts\development\run_app.bat %*
)

REM Check if the script ran successfully
if errorlevel 1 (
    echo.
    echo [ERROR] File Combiner App encountered an error
    echo [INFO] Check the logs above for details
    pause
    exit /b 1
) else (
    echo.
    echo [SUCCESS] File Combiner App completed successfully!
)

REM Keep window open if run directly
if "%0" == "%~dpnx0" (
    echo.
    echo [INFO] Press any key to exit...
    pause > nul
)