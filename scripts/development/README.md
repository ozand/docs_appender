# Development Scripts

This directory contains scripts for development and testing purposes.

## Available Scripts

### Windows (`.bat` files)

- `run_app.bat` - Runs both backend and frontend services
- `run_backend.bat` - Runs the backend service
- `run_frontend.bat` - Runs the frontend service
- `run_tests.bat` - Runs the test suite
- `smart_start.bat` - Smart setup and run script with optional cleanup

### Unix/Linux/macOS (`.sh` files)

- `run_app.sh` - Runs both backend and frontend services
- `run_tests.sh` - Runs the test suite
- `smart_start.sh` - Smart setup and run script with optional cleanup

## Usage

To run any of these scripts, navigate to the project root directory and execute:

```bash
# On Windows
scripts\\development\\run_app.bat

# On Unix/Linux/macOS
./scripts/development/run_app.sh
```

### Smart Start Scripts

The smart start scripts provide an automated way to set up and run the application:

```bash
# On Windows
scripts\\development\\smart_start.bat [--clear] [--help]

# On Unix/Linux/macOS
./scripts/development/smart_start.sh [--clear] [--help]
```

Options:
- `--clear`: Perform full cleanup before starting (removes cache, temporary files, and virtual environments)
- `--help`: Show help information

These scripts will:
1. Check for required tools (Python, uv)
2. Create virtual environments if they don't exist
3. Install dependencies
4. Launch the application