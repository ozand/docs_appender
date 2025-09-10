---
title:: Development Scripts Documentation
---

# Development Scripts Documentation

This directory contains auxiliary technical scripts for the File Combiner Application project. These scripts are designed to support development workflows, automate common tasks, and provide unified interfaces for complex operations.

## 📋 Table of Contents

- [Unified Application Launcher](#unified-application-launcher)
- [Knowledge Base Management](#knowledge-base-management)
- [Development Utilities](#development-utilities)
- [Usage Guidelines](#usage-guidelines)

## 🚀 Unified Application Launcher

### Overview

The [`start_app.py`](scripts/development/start_app.py) script provides a unified interface to start the application in different modes, replacing multiple scattered startup scripts with a single, comprehensive solution.

### Features

- **Multiple Startup Modes**: Backend only, frontend only, both services together, or Docker Compose
- **Dependency Management**: Automatic dependency installation with `uv sync`
- **Configurable Hosts & Ports**: Customizable network configuration for both services
- **Process Management**: Proper subprocess handling with logging and error reporting
- **Docker Integration**: Seamless Docker Compose integration with optional image building
- **Frontend Shutdown Button**: Streamlit app includes a shutdown button for graceful service termination
- **Cross-Platform Support**: Works on Windows, macOS, and Linux

### Command-Line Interface

```bash
python scripts/development/start_app.py [mode] [options]
```

#### Available Modes

| Mode | Description |
|------|-------------|
| `backend` | Start only the backend service |
| `frontend` | Start only the frontend service |
| `both` | Start both backend and frontend services |
| `docker` | Start services using Docker Compose |

#### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--install-deps` | Install dependencies before starting services | `False` |
| `--backend-host` | Host for backend service | `127.0.0.1` |
| `--backend-port` | Port for backend service | `8000` |
| `--frontend-host` | Host for frontend service | `127.0.0.1` |
| `--frontend-port` | Port for frontend service | `8501` |
| `--build` | Build Docker images before starting (docker mode only) | `False` |
| `--project-root` | Project root directory | Current directory |

### Usage Examples

#### Basic Usage

```bash
# Start both services with default settings
python scripts/development/start_app.py both

# Start only the backend service
python scripts/development/start_app.py backend

# Start only the frontend service
python scripts/development/start_app.py frontend

# Start using Docker Compose
python scripts/development/start_app.py docker
```

#### Advanced Configuration

```bash
# Start both services with custom ports
python scripts/development/start_app.py both --backend-port 8080 --frontend-port 3000

# Start with dependency installation
python scripts/development/start_app.py both --install-deps

# Start backend on all interfaces
python scripts/development/start_app.py backend --backend-host 0.0.0.0

# Docker with image building
python scripts/development/start_app.py docker --build
```

#### Development Workflow Examples

```bash
# Quick development setup (install deps and start both)
python scripts/development/start_app.py both --install-deps

# Frontend-only development (assuming backend is already running)
python scripts/development/start_app.py frontend --frontend-port 3001

# Backend API development with custom configuration
python scripts/development/start_app.py backend --backend-host 0.0.0.0 --backend-port 8080
```

#### Frontend Shutdown Feature

When starting the frontend service with `start_app.py`, a "Shutdown Application" button will appear in the Streamlit sidebar.
This button allows users to gracefully shut down all application services directly from the UI:

1. Click the "Shutdown Application" button in the sidebar
2. Confirm the shutdown action in the confirmation dialog
3. The application services will be terminated gracefully

This feature is only available when the frontend is started through `start_app.py` as it sets an environment variable
that enables the shutdown functionality in the Streamlit app.

### Service Information

When started successfully, the script provides the following service URLs:

- **Backend API**: `http://{backend_host}:{backend_port}`
- **Frontend UI**: `http://{frontend_host}:{frontend_port}`

Default URLs:
- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:8501`

### Requirements

- Python 3.7+
- [`uv`](https://docs.astral.sh/uv/) package manager
- Docker and Docker Compose (for docker mode)

### Installation

1. Install `uv` if not already installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. The script will automatically check for and install dependencies when using `--install-deps` flag

### Troubleshooting

#### Common Issues

1. **"uv command not found"**
   - Install `uv` using the command above
   - Ensure `uv` is in your PATH

2. **"Backend directory not found"**
   - Ensure you're running from the project root
   - Check that `backend/` directory exists

3. **"Frontend directory not found"**
   - Ensure you're running from the project root
   - Check that `frontend/` directory exists

4. **"Docker Compose file not found"**
   - Ensure [`docker-compose.yml`](docker-compose.yml) exists in project root
   - Check Docker and Docker Compose are installed

5. **Dependency installation fails**
   - Check internet connectivity
   - Verify `pyproject.toml` files in backend/frontend directories
   - Try manual installation: `cd backend && uv sync` or `cd frontend && uv sync`

#### Service-Specific Issues

**Backend Service:**
- Check backend logs for import errors
- Verify `PYTHONPATH` is set correctly
- Ensure backend dependencies are installed

**Frontend Service:**
- Check frontend logs for Streamlit errors
- Verify `app.py` exists in frontend directory
- Ensure frontend dependencies are installed

### Comparison with Other Startup Methods

| Method | Pros | Cons | Use Case |
|--------|------|------|----------|
| **Unified Script** | Single command, dependency management, flexible configuration | Requires Python | Development, testing |
| **Docker Compose** | Consistent environment, production-ready | Requires Docker, slower startup | Production, CI/CD |
| **Manual Startup** | Full control, no dependencies | Complex, error-prone | Advanced debugging |
| **Backend BAT Script** | Windows-specific, simple | Limited functionality | Windows-only backend |

### Integration with Development Workflow

The unified script integrates seamlessly with the project's development workflow:

1. **Pre-commit Hooks**: Can be used in pre-commit hooks for testing
2. **CI/CD Pipelines**: Provides consistent startup for automated testing
3. **Development Environment**: Quick setup for new developers
4. **Debugging**: Easy service restart during development
## ⏹ Unified Application Shutdown

### Overview

The [`stop_app.py`](scripts/development/stop_app.py) script provides a unified interface to stop the application services, replacing manual process termination with a single, comprehensive solution.

### Features

- **Multiple Shutdown Modes**: Backend only, frontend only, both services together, or Docker Compose
- **Process Identification**: Automatically finds running services by command line patterns
- **Graceful Termination**: Uses proper process termination signals for clean shutdown
- **Process Tree Handling**: Terminates child processes along with parent processes
- **Service Status Checking**: List running services to verify what needs to be stopped
- **Cross-Platform Support**: Works on Windows, macOS, and Linux

### Command-Line Interface

```bash
python scripts/development/stop_app.py [mode] [options]
```

#### Available Modes

| Mode | Description |
|------|-------------|
| `backend` | Stop only the backend service |
| `frontend` | Stop only the frontend service |
| `both` | Stop both backend and frontend services |
| `docker` | Stop services using Docker Compose |
| `all` | Stop all services (local and Docker) |
| `list` | List all currently running services (default) |

#### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--project-root` | Project root directory | Current directory |

### Usage Examples

#### Basic Usage

```bash
# List all running services (default behavior)
python scripts/development/stop_app.py

# Stop both services
python scripts/development/stop_app.py both

# Stop only the backend service
python scripts/development/stop_app.py backend

# Stop only the frontend service
python scripts/development/stop_app.py frontend

# Stop using Docker Compose
python scripts/development/stop_app.py docker

# Stop all services
python scripts/development/stop_app.py all
```

### Requirements

- Python 3.7+
- [`psutil`](https://pypi.org/project/psutil/) package (automatically installed with dev dependencies)
- Docker and Docker Compose (for docker mode)

### Installation

The `psutil` dependency is included in the development dependencies:
```bash
uv sync
```

If needed separately:
```bash
uv add --dev psutil
```

### Troubleshooting

#### Common Issues

1. **"psutil module is required but not found"**
   - Run `uv sync` to install development dependencies
   - Or install separately: `uv add --dev psutil`

2. **"Permission denied" when stopping processes**
   - On Unix systems, you may need to run with appropriate permissions for processes owned by other users
   - On Windows, run the command prompt as Administrator if needed

3. **Processes not stopping**
   - Some processes might be stuck or unresponsive
   - Use system process manager to manually terminate stubborn processes
   - Check if the processes are actually running with `stop_app.py list`

### Integration with Development Workflow

The unified shutdown script integrates seamlessly with the project's development workflow:

1. **Development Cleanup**: Easy cleanup after development sessions
2. **CI/CD Pipelines**: Ensures clean shutdown in automated testing
3. **Service Management**: Quick restart of services during development
4. **Resource Management**: Frees up system resources when services aren't needed

### Comparison with Other Shutdown Methods

| Method | Pros | Cons | Use Case |
|--------|------|------|----------|
| **Unified Script** | Single command, automatic process detection, clean shutdown | Requires Python | Development, testing |
| **Manual Ctrl+C** | Immediate, no tools needed | Only works for foreground processes, no cleanup | Quick testing |
| **Task Manager/System Monitor** | Works for any process | Manual, not scriptable | Emergency situations |
| **Docker Compose** | Built-in shutdown | Only for Docker services | Docker-based development |

## 🗃️ Knowledge Base Management

### validate_kb.py

Validates the integrity of the project knowledge base by checking:
- Link integrity and formatting
- File structure compliance
- Properties schema validation
- Status correctness

Usage:
```bash
python scripts/development/validate_kb.py
```

## 🔧 Development Utilities

### generate_logseq_config.py

Generates Logseq configuration files for the project knowledge base.

### sync_git_kb.py

Synchronizes knowledge base files with Git repository state.

### parser_script.py

Utility script for parsing and processing project files.

## 📋 Usage Guidelines

### Best Practices

1. **Always check script help**: Use `--help` flag to see available options
2. **Use absolute paths**: When specifying project root or file paths
3. **Monitor logs**: Check console output for errors and warnings
4. **Test in isolation**: Test individual services before starting both
5. **Keep dependencies updated**: Use `--install-deps` periodically

### Script Development

When creating new scripts in this directory:

1. Follow the [project quality guidelines](pages/rules.01-quality-guideline.md)
2. Include comprehensive docstrings and help text
3. Use argument parsing for CLI interfaces
4. Implement proper error handling and logging
5. Add scripts to this README documentation

### Maintenance

- Scripts are automatically excluded from production builds
- Regular dependency audits should include development scripts
- Archive unused scripts to `scripts/development/archive/`
- Update documentation when modifying script functionality

## 🔗 Related Documentation

- [Project Quality Guidelines](pages/rules.01-quality-guideline.md)
- [Scripts Structure Guidelines](pages/rules.02-scripts-structure.md)
- [Docker Compose Configuration](docker-compose.yml)
- [Backend Start Script](backend/start_server.bat)
- [E2E Testing Guidelines](pages/rules.03-e2e-tests-guidline.md)
- [Service Shutdown Script](scripts/development/stop_app.py)

## 📞 Support

For issues with development scripts:
1. Check the troubleshooting section above
2. Review script logs for error messages
3. Consult the related documentation
4. Create an issue in the project repository

---
*Last updated: September 10, 2025*