#!/usr/bin/env python3
"""
Test script for verifying the frontend shutdown functionality integration
with the stop_app.py script.
"""

import os
import sys
import time
import subprocess
import requests
from pathlib import Path

def test_shutdown_functionality():
    """Test the shutdown functionality integration."""
    print("Testing frontend shutdown functionality integration...")
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    frontend_dir = project_root / "frontend"
    
    # Check if we're in the correct directory
    if not (frontend_dir / "app.py").exists():
        print(f"Error: Could not find app.py in {frontend_dir}")
        return False
    
    print(f"Project root: {project_root}")
    print(f"Frontend directory: {frontend_dir}")
    
    # Start the frontend service with shutdown enabled
    print("Starting frontend service with shutdown enabled...")
    env = os.environ.copy()
    env["STREAMLIT_SHUTDOWN_ENABLED"] = "true"
    
    try:
        # Start the frontend service
        frontend_process = subprocess.Popen(
            [
                sys.executable, "-m", "streamlit", "run", "app.py",
                "--server.port", "8502",
                "--server.headless", "true"
            ],
            cwd=frontend_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"Frontend process started with PID: {frontend_process.pid}")
        
        # Wait for the service to start
        print("Waiting for frontend service to start...")
        time.sleep(10)
        
        # Check if the service is running
        try:
            response = requests.get("http://localhost:8502/healthz", timeout=5)
            if response.status_code == 200:
                print("Frontend service is running and responding")
            else:
                print(f"Frontend service responded with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Could not connect to frontend service: {e}")
        
        # Try to shutdown the service using stop_app.py
        print("Attempting to shutdown frontend service using stop_app.py...")
        stop_process = subprocess.run(
            [
                sys.executable, "scripts/development/stop_app.py", "frontend"
            ],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        print(f"Stop script stdout: {stop_process.stdout}")
        print(f"Stop script stderr: {stop_process.stderr}")
        print(f"Stop script return code: {stop_process.returncode}")
        
        # Wait a bit for the process to terminate
        time.sleep(5)
        
        # Check if the process is still running
        if frontend_process.poll() is None:
            print("Frontend process is still running, terminating...")
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=10)
                print("Frontend process terminated successfully")
            except subprocess.TimeoutExpired:
                print("Frontend process did not terminate, killing...")
                frontend_process.kill()
                frontend_process.wait()
        else:
            print("Frontend process has terminated")
            
        return True
        
    except Exception as e:
        print(f"Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_shutdown_functionality()
    if success:
        print("Test completed successfully")
        sys.exit(0)
    else:
        print("Test failed")
        sys.exit(1)