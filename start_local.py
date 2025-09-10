#!/usr/bin/env python3
"""
Unified Local Startup Script for File Combiner Application

This script provides a simple way to start both backend and frontend services
for local development without authentication requirements.

Usage:
    python start_local.py

The script will:
1. Start the backend service on http://127.0.0.1:8000
2. Start the frontend service on http://127.0.0.1:8501
3. Keep both services running until interrupted
"""

import subprocess
import sys
import os
import time
from pathlib import Path


def start_service(name, cmd, cwd, env=None):
    """Start a service and return the process."""
    print(f"\n🚀 Starting {name}...")
    
    # Set environment variables
    process_env = os.environ.copy()
    process_env["SKIP_AUTH"] = "true"  # Disable authentication for local development
    if env:
        process_env.update(env)
    
    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=process_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Give the process a moment to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✅ {name} started successfully!")
            print(f"   PID: {process.pid}")
            return process
        else:
            print(f"❌ {name} failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting {name}: {e}")
        return None


def main():
    """Main function to start both services."""
    print("🎯 File Combiner - Local Development Startup")
    print("=" * 50)
    
    project_root = Path.cwd()
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"
    
    # Check if directories exist
    if not backend_dir.exists():
        print(f"❌ Backend directory not found: {backend_dir}")
        return 1
        
    if not frontend_dir.exists():
        print(f"❌ Frontend directory not found: {frontend_dir}")
        return 1
    
    processes = []
    
    try:
        # Start backend
        backend_cmd = [
            "uv", "run", "python", "-m", "uvicorn",
            "src.backend.main:app",
            "--host", "127.0.0.1",
            "--port", "8000"
        ]
        backend_env = {"PYTHONPATH": "src"}
        
        backend_process = start_service(
            "Backend", 
            backend_cmd, 
            backend_dir, 
            backend_env
        )
        
        if not backend_process:
            return 1
            
        processes.append(("Backend", backend_process, "http://127.0.0.1:8000"))
        
        # Wait a bit for backend to fully start
        time.sleep(3)
        
        # Start frontend
        frontend_cmd = [
            "uv", "run", "streamlit", "run", "app.py",
            "--server.address", "127.0.0.1",
            "--server.port", "8501"
        ]
        
        frontend_process = start_service(
            "Frontend", 
            frontend_cmd, 
            frontend_dir
        )
        
        if not frontend_process:
            # Kill backend if frontend fails
            backend_process.terminate()
            return 1
            
        processes.append(("Frontend", frontend_process, "http://127.0.0.1:8501"))
        
        # Print summary
        print("\n" + "=" * 50)
        print("🎉 Both services started successfully!")
        print("\n📍 Service URLs:")
        for name, _, url in processes:
            print(f"   • {name}: {url}")
        
        print("\n📝 Authentication: DISABLED for local development")
        print("🛑 Press Ctrl+C to stop all services")
        print("=" * 50 + "\n")
        
        # Monitor processes
        while True:
            for name, process, url in processes:
                if process.poll() is not None:
                    print(f"\n❌ {name} process died (exit code: {process.returncode})")
                    print("🛑 Stopping other services...")
                    
                    # Kill other processes
                    for _, other_process, _ in processes:
                        if other_process != process:
                            try:
                                other_process.terminate()
                                other_process.wait(timeout=5)
                            except:
                                try:
                                    other_process.kill()
                                except:
                                    pass
                    
                    return 1
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        
        for name, process, _ in processes:
            print(f"   Stopping {name}...")
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        print("\n✅ All services stopped.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        
        # Clean up processes
        for name, process, _ in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        return 1


if __name__ == "__main__":
    sys.exit(main())