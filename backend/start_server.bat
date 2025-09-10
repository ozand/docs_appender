@echo off
set PYTHONPATH=src
uv run python -m uvicorn src.backend.main:app --host 0.0.0.0 --port 8000