#!/bin/bash
# run_tests.sh - Script to run tests for the File Combiner project

echo "========================================"
echo "Running tests for shared module..."
echo "========================================"
cd backend
uv run pytest ../tests/shared -v
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Tests for shared module failed."
    exit 1
fi
cd ..

echo ""
echo "========================================"
echo "All tests passed successfully!"
echo "========================================"