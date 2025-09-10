#!/usr/bin/env python3
"""
Unified Shutdown Script for File Combiner Application

This script provides a unified interface to stop the application services:
- Backend service
- Frontend service
- Both services together
- Docker Compose services

The script handles process identification, graceful shutdown, and cleanup.

Usage:
    python scripts/development/stop_app.py [mode] [options]

Examples:
    python scripts/development/stop_app.py --help
    python scripts/development/stop_app.py backend
    python scripts/development/stop_app.py frontend
    python scripts/development/stop_app.py both
    python scripts/development/stop_app.py docker
"""

import argparse
import subprocess
import sys
import os
import signal
import psutil
import time
from pathlib import Path
from typing import List, Optional


class AppStopper:
    """Manages the stopping of different components of the application."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_dir = project_root / "backend"
        self.frontend_dir = project_root / "frontend"

    def _find_processes_by_cmdline(self, pattern: str) -> List[psutil.Process]:
        """Find processes by command line pattern."""
        matching_processes = []
        for proc in psutil.process_iter(['pid', 'cmdline']):
            try:
                if proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    if pattern in cmdline:
                        matching_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return matching_processes

    def _kill_process_tree(self, pid: int) -> bool:
        """Kill a process and all its children."""
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            
            # Terminate children first
            for child in children:
                try:
                    child.terminate()
                except psutil.NoSuchProcess:
                    pass
            
            # Terminate parent
            parent.terminate()
            
            # Wait for processes to terminate
            gone, alive = psutil.wait_procs(children + [parent], timeout=3)
            
            # Force kill any remaining processes
            for p in alive:
                try:
                    p.kill()
                except psutil.NoSuchProcess:
                    pass
            
            return True
        except psutil.NoSuchProcess:
            print(f"Process with PID {pid} not found")
            return False
        except Exception as e:
            print(f"Error killing process tree: {e}")
            return False

    def stop_backend(self) -> bool:
        """Stop the backend service."""
        print("Stopping backend service...")
        
        # Find backend processes
        backend_processes = self._find_processes_by_cmdline("uv run python -m uvicorn src.backend.main:app")
        
        if not backend_processes:
            print("No backend processes found")
            return True
            
        # Kill processes
        success = True
        for proc in backend_processes:
            try:
                print(f"Terminating backend process PID {proc.pid}")
                if not self._kill_process_tree(proc.pid):
                    success = False
            except Exception as e:
                print(f"Error terminating backend process: {e}")
                success = False
                
        if success:
            print("Backend service stopped successfully")
        else:
            print("Some backend processes may still be running")
            
        return success

    def stop_frontend(self) -> bool:
        """Stop the frontend service."""
        print("Stopping frontend service...")
        
        # Find frontend processes
        frontend_processes = self._find_processes_by_cmdline("uv run streamlit run app.py")
        
        if not frontend_processes:
            print("No frontend processes found")
            return True
            
        # Kill processes
        success = True
        for proc in frontend_processes:
            try:
                print(f"Terminating frontend process PID {proc.pid}")
                if not self._kill_process_tree(proc.pid):
                    success = False
            except Exception as e:
                print(f"Error terminating frontend process: {e}")
                success = False
                
        if success:
            print("Frontend service stopped successfully")
        else:
            print("Some frontend processes may still be running")
            
        return success

    def stop_both(self) -> bool:
        """Stop both backend and frontend services."""
        print("Stopping both backend and frontend services...")
        
        backend_success = self.stop_backend()
        frontend_success = self.stop_frontend()
        
        if backend_success and frontend_success:
            print("Both services stopped successfully!")
            return True
        else:
            print("Some services may still be running")
            return False

    def stop_docker(self) -> bool:
        """Stop services using Docker Compose."""
        print("Stopping services with Docker Compose...")
        
        # Check if docker-compose.yml exists
        compose_file = self.project_root / "docker-compose.yml"
        if not compose_file.exists():
            print(f"Docker Compose file not found: {compose_file}")
            return False
            
        # Stop services
        cmd = ["docker-compose", "down"]
        try:
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            if result.returncode != 0:
                print("Failed to stop Docker Compose services:")
                print(result.stderr)
                return False
            print("Docker Compose services stopped successfully")
            return True
        except Exception as e:
            print(f"Failed to stop Docker Compose: {e}")
            return False

    def stop_all(self) -> bool:
        """Stop all running services (both local and Docker)."""
        print("Stopping all services...")
        
        # Stop local services
        local_success = self.stop_both()
        
        # Stop Docker services
        docker_success = self.stop_docker()
        
        if local_success and docker_success:
            print("All services stopped successfully!")
            return True
        else:
            print("Some services may still be running")
            return False

    def list_running_services(self) -> None:
        """List all running services."""
        print("Checking for running services...")
        
        # Check for backend processes
        backend_processes = self._find_processes_by_cmdline("uv run python -m uvicorn src.backend.main:app")
        if backend_processes:
            print("Backend services running:")
            for proc in backend_processes:
                try:
                    print(f"  PID {proc.pid}: {' '.join(proc.cmdline())}")
                except Exception as e:
                    print(f"  PID {proc.pid}: (error getting command line)")
        else:
            print("No backend services running")
            
        # Check for frontend processes
        frontend_processes = self._find_processes_by_cmdline("uv run streamlit run app.py")
        if frontend_processes:
            print("Frontend services running:")
            for proc in frontend_processes:
                try:
                    print(f"  PID {proc.pid}: {' '.join(proc.cmdline())}")
                except Exception as e:
                    print(f"  PID {proc.pid}: (error getting command line)")
        else:
            print("No frontend services running")
            
        # Check for Docker containers
        try:
            result = subprocess.run(["docker-compose", "ps"], cwd=self.project_root, capture_output=True, text=True)
            if result.returncode == 0 and "Name" in result.stdout:
                print("Docker containers running:")
                print(result.stdout)
            else:
                print("No Docker containers running")
        except Exception as e:
            print(f"Error checking Docker containers: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Unified Shutdown Script for File Combiner Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "mode",
        nargs='?',
        choices=["backend", "frontend", "both", "docker", "all", "list"],
        default="list",
        help="Shutdown mode: backend, frontend, both services, docker compose, all services, or list running services"
    )
    
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Check if psutil is available
    try:
        import psutil
    except ImportError:
        print("Error: psutil module is required but not found.")
        print("Install it with: pip install psutil")
        sys.exit(1)
    
    stopper = AppStopper(args.project_root)
    
    # If no mode specified, list running services
    if args.mode == "list":
        stopper.list_running_services()
        sys.exit(0)
    
    success = False
    if args.mode == "backend":
        success = stopper.stop_backend()
    elif args.mode == "frontend":
        success = stopper.stop_frontend()
    elif args.mode == "both":
        success = stopper.stop_both()
    elif args.mode == "docker":
        success = stopper.stop_docker()
    elif args.mode == "all":
        success = stopper.stop_all()
    
    if success:
        print("\n✅ Application services stopped successfully!")
        sys.exit(0)
    else:
        print("\n❌ Failed to stop application services!")
        sys.exit(1)


if __name__ == "__main__":
    main()