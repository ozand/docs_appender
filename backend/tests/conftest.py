"""
Pytest configuration and shared fixtures for backend unit tests.

This module provides common test fixtures and configuration for FastAPI backend tests,
including TestClient setup and test data management.
"""

import asyncio
import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

# Set test environment
os.environ["TESTING"] = "true"

# Add src directory to Python path for imports
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backend.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """Create a FastAPI TestClient for testing."""
    with TestClient(app) as test_client:
        yield test_client
