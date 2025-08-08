@echo off
REM run_tests.bat - Script to run tests for the File Combiner project

echo ========================================
echo Running tests for shared module...
echo ========================================
cd backend
call uv run pytest ../tests/shared -v
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Tests for shared module failed.
    exit /b %errorlevel%
)
cd ..

echo.
echo ========================================
echo All tests passed successfully!
echo ========================================