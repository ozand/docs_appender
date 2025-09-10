#!/usr/bin/env python3
"""
Unified Startup Script for File Combiner Application

This script provides a unified interface to start the application in different modes:
- Backend only
- Frontend only
- Both services together
- Docker Compose (primary method)

The script handles environment setup, dependency management, and process management.

Usage:
    python scripts/development/start_app.py [mode] [options]

Examples:
    python scripts/development/start_app.py --help
    python scripts/development/start_app.py backend
    python scripts/development/start_app.py frontend
    python scripts/development/start_app.py both
    python scripts/development/start_app.py docker
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Optional
import time


class AppLauncher:
    """Manages the launching of different components of the application."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_dir = project_root / "backend"
        self.frontend_dir = project_root / "frontend"

    def _run_command(self, cmd: List[str], cwd: Path, env_vars: Optional[dict] = None) -> subprocess.Popen:
        """Run a command in a subprocess."""
        env = os.environ.copy()
        if env_vars:
            env.update(env_vars)
        
        print(f"Running command: {' '.join(cmd)}")
        print(f"In directory: {cwd}")
        
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        return process

    def _check_dependencies(self, directory: Path) -> bool:
        """Check if dependencies are installed in the specified directory."""
        try:
            result = subprocess.run(
                ["uv", "pip", "list"],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"Timeout checking dependencies in {directory}")
            return False
        except FileNotFoundError:
            print("uv command not found. Please install uv.")
            return False

    def _install_dependencies(self, directory: Path) -> bool:
        """Install dependencies using uv in the specified directory."""
        print(f"Installing dependencies in {directory}...")
        try:
            result = subprocess.run(
                ["uv", "sync"],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            if result.returncode != 0:
                print(f"Failed to install dependencies in {directory}:")
                print(result.stderr)
                return False
            print(f"Dependencies installed successfully in {directory}")
            return True
        except subprocess.TimeoutExpired:
            print(f"Timeout installing dependencies in {directory}")
            return False
        except FileNotFoundError:
            print("uv command not found. Please install uv.")
            return False

    def start_backend(self, install_deps: bool = False, host: str = "127.0.0.1", port: int = 8000) -> bool:
        """Start the backend service."""
        print("Starting backend service...")
        
        # Check if backend directory exists
        if not self.backend_dir.exists():
            print(f"Backend directory not found: {self.backend_dir}")
            return False
            
        # Install dependencies if requested
        if install_deps:
            if not self._install_dependencies(self.backend_dir):
                return False
        elif not self._check_dependencies(self.backend_dir):
            print("Backend dependencies not found. Consider using --install-deps flag.")
            return False

        # Set environment variables
        env_vars = {
            "PYTHONPATH": "src"
        }
        
        # Start the backend service
        cmd = [
            "uv", "run", "python", "-m", "uvicorn", 
            "src.backend.main:app", 
            "--host", host, 
            "--port", str(port)
        ]
        
        try:
            process = self._run_command(cmd, self.backend_dir, env_vars)
            print(f"Backend started successfully on http://{host}:{port}")
            print("Backend PID:", process.pid)
            return True
        except Exception as e:
            print(f"Failed to start backend: {e}")
            return False

    def start_frontend(self, install_deps: bool = False, host: str = "127.0.0.1", port: int = 8501) -> bool:
        """Start the frontend service."""
        print("Starting frontend service...")
        
        # Check if frontend directory exists
        if not self.frontend_dir.exists():
            print(f"Frontend directory not found: {self.frontend_dir}")
            return False
            
        # Install dependencies if requested
        if install_deps:
            if not self._install_dependencies(self.frontend_dir):
                return False
        elif not self._check_dependencies(self.frontend_dir):
            print("Frontend dependencies not found. Consider using --install-deps flag.")
            return False

        # Start the frontend service
        cmd = [
            "uv", "run", "streamlit", "run", "app.py",
            "--server.address", host,
            "--server.port", str(port)
        ]
        
        # Set environment variable to enable shutdown functionality
        env_vars = {
            "STREAMLIT_SHUTDOWN_ENABLED": "true"
        }
        
        try:
            process = self._run_command(cmd, self.frontend_dir, env_vars)
            print(f"Frontend started successfully on http://{host}:{port}")
            print("Frontend PID:", process.pid)
            return True
        except Exception as e:
            print(f"Failed to start frontend: {e}")
            return False

    def start_both(self, install_deps: bool = False, backend_host: str = "127.0.0.1", 
                   backend_port: int = 8000, frontend_host: str = "127.0.0.1", frontend_port: int = 8501) -> bool:
        """Start both backend and frontend services."""
        print("Starting both backend and frontend services...")
        
        # Start backend
        backend_success = self.start_backend(install_deps, backend_host, backend_port)
        if not backend_success:
            print("Failed to start backend. Aborting.")
            return False
            
        # Add a small delay to ensure backend starts first
        time.sleep(2)
        
        # Start frontend
        frontend_success = self.start_frontend(install_deps, frontend_host, frontend_port)
        if not frontend_success:
            print("Failed to start frontend.")
            return False
            
        print("Both services started successfully!")
        print(f"Backend: http://{backend_host}:{backend_port}")
        print(f"Frontend: http://{frontend_host}:{frontend_port}")
        return True

    def start_docker(self, build: bool = False) -> bool:
        """Start services using Docker Compose."""
        print("Starting services with Docker Compose...")
        
        # Check if docker-compose.yml exists
        compose_file = self.project_root / "docker-compose.yml"
        if not compose_file.exists():
            print(f"Docker Compose file not found: {compose_file}")
            return False
            
        # Build images if requested
        cmd = ["docker-compose"]
        if build:
            cmd.extend(["build"])
            try:
                result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
                if result.returncode != 0:
                    print("Failed to build Docker images:")
                    print(result.stderr)
                    return False
                print("Docker images built successfully")
            except Exception as e:
                print(f"Failed to build Docker images: {e}")
                return False
        
        # Start services
        cmd = ["docker-compose", "up"]
        try:
            process = self._run_command(cmd, self.project_root)
            print("Docker Compose started successfully")
            print("Services:")
            print("  Backend: http://localhost:8000")
            print("  Frontend: http://localhost:8501")
            print("Docker Compose PID:", process.pid)
            return True
        except Exception as e:
            print(f"Failed to start Docker Compose: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Unified Startup Script for File Combiner Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "mode",
        choices=["backend", "frontend", "both", "docker"],
        help="Startup mode: backend, frontend, both services, or docker compose"
    )
    
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install dependencies before starting services"
    )
    
    parser.add_argument(
        "--backend-host",
        default="127.0.0.1",
        help="Host for backend service (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--backend-port",
        type=int,
        default=8000,
        help="Port for backend service (default: 8000)"
    )
    
    parser.add_argument(
        "--frontend-host",
        default="127.0.0.1",
        help="Host for frontend service (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--frontend-port",
        type=int,
        default=8501,
        help="Port for frontend service (default: 8501)"
    )
    
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build Docker images before starting (only for docker mode)"
    )
    
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)"
    )
    
    args = parser.parse_args()
    
    launcher = AppLauncher(args.project_root)
    
    success = False
    if args.mode == "backend":
        success = launcher.start_backend(
            install_deps=args.install_deps,
            host=args.backend_host,
            port=args.backend_port
        )
    elif args.mode == "frontend":
        success = launcher.start_frontend(
            install_deps=args.install_deps,
            host=args.frontend_host,
            port=args.frontend_port
        )
    elif args.mode == "both":
        success = launcher.start_both(
            install_deps=args.install_deps,
            backend_host=args.backend_host,
            backend_port=args.backend_port,
            frontend_host=args.frontend_host,
            frontend_port=args.frontend_port
        )
    elif args.mode == "docker":
        success = launcher.start_docker(build=args.build)
    
    if success:
        print("\n✅ Application started successfully!")
        sys.exit(0)
    else:
        print("\n❌ Failed to start application!")
        sys.exit(1)


if __name__ == "__main__":
    main()