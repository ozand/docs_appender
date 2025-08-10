#!/bin/bash

# Smart Start script for File Combiner App (Unix/Linux/macOS version)

set -e  # Exit on any error

# Function to print colored output
print_status() {
    echo -e "\n\e[1;36m[$1]\e[0m $2"
}

print_success() {
    echo -e "\e[1;32m[SUCCESS]\e[0m $1"
}

print_error() {
    echo -e "\e[1;31m[ERROR]\e[0m $1"
}

print_info() {
    echo -e "\e[1;33m[INFO]\e[0m $1"
}

# Change to project directory
cd "$(dirname "$0")/../.."

print_status "ROCKET" "Smart Start for File Combiner App"
echo "--------------------------------------------------"

# Parse command line arguments
CLEAR_MODE=false
SHOW_HELP=false

for arg in "$@"; do
    case $arg in
        --clear)
            CLEAR_MODE=true
            shift
            ;;
        --help)
            SHOW_HELP=true
            shift
            ;;
        *)
            print_error "Unknown parameter: $arg"
            print_info "Use: $0 --help"
            exit 1
            ;;
    esac
done

# Show help if requested
if [ "$SHOW_HELP" = true ]; then
    echo "[HELP] Smart Start Usage:"
    echo
    echo "  ./smart_start.sh          - Normal startup"
    echo "  ./smart_start.sh --clear  - Startup with full cleanup"
    echo "  ./smart_start.sh --help   - Show this help"
    echo
    echo "[INFO] --clear mode cleans:"
    echo "  - __pycache__ directories and .pyc files"
    echo "  - All logs and temporary files"
    echo "  - uv cache directories"
    echo "  - Virtual environments (.venv directories"
    exit 0
fi

# Check if required tools are available
if ! command -v python3 &> /dev/null; then
    print_error "Python not found. Install Python and add to PATH."
    exit 1
fi

if ! command -v uv &> /dev/null; then
    print_error "uv not found. Install uv (https://github.com/astral-sh/uv) and add to PATH."
    exit 1
fi

# Perform cleanup if --clear mode is active
if [ "$CLEAR_MODE" = true ]; then
    print_status "CLEANUP" "Performing full cleanup..."
    
    # Clean __pycache__ directories
    print_status "CLEANUP" "Removing __pycache__ directories..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    
    # Clean .pyc files
    print_status "CLEANUP" "Removing .pyc files..."
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    
    # Clean logs
    print_status "CLEANUP" "Removing log files..."
    find . -type f -name "*.log" -delete 2>/dev/null || true
    
    # Clean temporary files
    print_status "CLEANUP" "Removing temporary files..."
    rm -f temp_* tmp_* 2>/dev/null || true
    
    # Clean uv cache directories
    print_status "CLEANUP" "Removing uv cache directories..."
    rm -rf backend/.uv frontend/.uv scripts/development/.uv 2>/dev/null || true
    
    # Clean virtual environments
    print_status "CLEANUP" "Removing virtual environments..."
    rm -rf backend/.venv frontend/.venv 2>/dev/null || true
    
    # Clean test cache directories
    print_status "CLEANUP" "Removing test cache directories..."
    rm -rf .pytest_cache .mypy_cache .ruff_cache 2>/dev/null || true
    
    print_success "Cleanup completed!"
    echo
fi

# Create virtual environments and install dependencies
print_status "SETUP" "Setting up backend environment..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_status "SETUP" "Creating virtual environment for backend..."
    uv venv
fi

print_status "SETUP" "Installing backend dependencies..."
uv sync

cd ..

print_status "SETUP" "Setting up frontend environment..."
cd frontend

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_status "SETUP" "Creating virtual environment for frontend..."
    uv venv
fi

print_status "SETUP" "Installing frontend dependencies..."
uv sync

cd ..

# Run the application
print_status "START" "Launching File Combiner App..."
./scripts/development/run_app.sh

print_success "File Combiner App completed successfully!"