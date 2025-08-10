#!/usr/bin/env python3
"""
Smart Start script for File Combiner App.
This script provides a Python-based alternative to the batch file for cross-platform compatibility.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_prerequisites():
    """Check if required tools are available."""
    # Check Python
    try:
        subprocess.run(
            [sys.executable, "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        print("[ERROR] Python not found. Install Python and add to PATH.")
        return False

    # Check uv
    try:
        subprocess.run(
            ["uv", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        print("[ERROR] uv not found. Install uv (https://github.com/astral-sh/uv) and add to PATH.")
        return False

    return True


def clean_project(project_root: Path):
    """Perform full cleanup of the project."""
    print("[CLEANUP] Performing full cleanup...")

    # Clean __pycache__ directories
    print("[CLEANUP] Removing __pycache__ directories...")
    for pycache_dir in project_root.rglob("__pycache__"):
        if pycache_dir.is_dir():
            print(f"  Removing: {pycache_dir}")
            shutil.rmtree(pycache_dir, ignore_errors=True)

    # Clean .pyc files
    print("[CLEANUP] Removing .pyc files...")
    for pyc_file in project_root.rglob("*.pyc"):
        if pyc_file.is_file():
            pyc_file.unlink()

    # Clean log files
    print("[CLEANUP] Removing log files...")
    for log_file in project_root.rglob("*.log"):
        if log_file.is_file():
            log_file.unlink()

    # Clean temporary files
    print("[CLEANUP] Removing temporary files...")
    for temp_file in project_root.glob("temp_*"):
        if temp_file.is_file():
            temp_file.unlink()
    for tmp_file in project_root.glob("tmp_*"):
        if tmp_file.is_file():
            tmp_file.unlink()

    # Clean uv cache directories
    print("[CLEANUP] Removing uv cache directories...")
    uv_cache_dirs = [
        project_root / "backend" / ".uv",
        project_root / "frontend" / ".uv",
        project_root / "scripts" / "development" / ".uv",
    ]
    for uv_cache in uv_cache_dirs:
        if uv_cache.exists():
            print(f"  Removing: {uv_cache}")
            shutil.rmtree(uv_cache, ignore_errors=True)

    # Clean virtual environments
    print("[CLEANUP] Removing virtual environments...")
    venv_dirs = [
        project_root / "backend" / ".venv",
        project_root / "frontend" / ".venv",
    ]
    for venv in venv_dirs:
        if venv.exists():
            print(f"  Removing: {venv}")
            shutil.rmtree(venv, ignore_errors=True)

    # Clean test cache directories
    print("[CLEANUP] Removing test cache directories...")
    cache_dirs = [
        project_root / ".pytest_cache",
        project_root / ".mypy_cache",
        project_root / ".ruff_cache",
    ]
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            print(f"  Removing: {cache_dir}")
            shutil.rmtree(cache_dir, ignore_errors=True)

    print("[SUCCESS] Cleanup completed!")


def setup_environments(project_root: Path):
    """Set up virtual environments and install dependencies."""
    # Backend setup
    print("[SETUP] Setting up backend environment...")
    backend_dir = project_root / "backend"
    os.chdir(backend_dir)

    # Create virtual environment if it doesn't exist
    venv_dir = backend_dir / ".venv"
    if not venv_dir.exists():
        print("[SETUP] Creating virtual environment for backend...")
        try:
            subprocess.run(["uv", "venv"], check=True)
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to create backend virtual environment")
            return False

    # Install dependencies
    print("[SETUP] Installing backend dependencies...")
    try:
        subprocess.run(["uv", "sync"], check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to install backend dependencies")
        return False

    # Frontend setup
    print("[SETUP] Setting up frontend environment...")
    frontend_dir = project_root / "frontend"
    os.chdir(frontend_dir)

    # Create virtual environment if it doesn't exist
    venv_dir = frontend_dir / ".venv"
    if not venv_dir.exists():
        print("[SETUP] Creating virtual environment for frontend...")
        try:
            subprocess.run(["uv", "venv"], check=True)
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to create frontend virtual environment")
            return False

    # Install dependencies
    print("[SETUP] Installing frontend dependencies...")
    try:
        subprocess.run(["uv", "sync"], check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to install frontend dependencies")
        return False

    return True


def run_application(project_root: Path):
    """Run the application using the existing run_app script."""
    print("[START] Launching File Combiner App...")
    run_app_script = project_root / "scripts" / "development" / "run_app.bat"
    
    if not run_app_script.exists():
        print("[ERROR] run_app.bat not found")
        return False
        
    try:
        # On Windows, we can call the batch file directly
        if os.name == "nt":
            subprocess.run([str(run_app_script)], check=True)
        else:
            print("[ERROR] This script is intended for Windows. Use run_app.sh on Unix-like systems.")
            return False
    except subprocess.CalledProcessError:
        print("[ERROR] File Combiner App encountered an error")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Smart Start for File Combiner App")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Perform full cleanup before starting"
    )
    parser.add_argument(
        "--help-script",
        action="store_true",
        help="Show help for this script"
    )

    args = parser.parse_args()

    if args.help_script:
        parser.print_help()
        return 0

    print()
    print("[ROCKET] Smart Start for File Combiner App")
    print("--------------------------------------------------")
    print()

    # Check prerequisites
    if not check_prerequisites():
        return 1

    # Get project root
    project_root = Path(__file__).parent.parent.parent.resolve()
    os.chdir(project_root)

    # Perform cleanup if requested
    if args.clear:
        clean_project(project_root)

    # Set up environments
    if not setup_environments(project_root):
        return 1

    # Run the application
    os.chdir(project_root)
    if not run_application(project_root):
        return 1

    print()
    print("[SUCCESS] File Combiner App completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())