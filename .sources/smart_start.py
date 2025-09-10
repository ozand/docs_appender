import argparse
import atexit
import http.client
import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Optional, Tuple


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
APP = SRC / "code2graf" / "code_analyzer" / "app.py"

STATE_DIR = ROOT / ".smart_start"
STATE_FILE = STATE_DIR / "smart_start.json"

DEFAULT_PORT_RANGE = (8501, 8599)
READINESS_TIMEOUT_SEC = 45
READINESS_POLL_INTERVAL_SEC = 1.0


def run(cmd: list[str], cwd: Optional[Path] = None, env: Optional[dict[str, str]] = None) -> int:
    print(f"[RUN] {' '.join(str(c) for c in cmd)}")
    try:
        return subprocess.call(cmd, cwd=str(cwd) if cwd else None, env=env)
    except KeyboardInterrupt:
        return 130


def ensure_pythonpath() -> None:
    # Prepend src to PYTHONPATH for absolute imports
    os.environ["PYTHONPATH"] = str(SRC) + os.pathsep + os.environ.get("PYTHONPATH", "")


def _is_port_free(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        try:
            return s.connect_ex((host, port)) != 0
        except OSError:
            return False


def _find_free_port(port_range: Tuple[int, int], host: str = "127.0.0.1") -> Optional[int]:
    start, end = port_range
    for port in range(start, end + 1):
        if _is_port_free(port, host=host):
            return port
    return None


def _http_check(host: str, port: int, path: str = "/", timeout: float = 1.0) -> bool:
    try:
        conn = http.client.HTTPConnection(host, port, timeout=timeout)
        conn.request("GET", path)
        resp = conn.getresponse()
        # Streamlit returns 200 on the root when ready
        return 200 <= resp.status < 500
    except OSError:
        return False
    except Exception:
        return False
    finally:
        try:
            conn.close()  # type: ignore[name-defined]
        except Exception:
            pass


def _save_state(data: dict[str, Any]) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as e:
        print(f"[WARN] Failed to persist state: {e}")


def _load_state() -> dict[str, Any]:
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {}


def _clear_state() -> None:
    try:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
    except OSError as e:
        print(f"[WARN] Failed to remove state file: {e}")


class FrontendProcess:
    def __init__(self) -> None:
        self.proc: Optional[subprocess.Popen] = None
        self.port: Optional[int] = None

    def start(self, port: int) -> bool:
        self.port = port
        python = sys.executable
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC) + os.pathsep + env.get("PYTHONPATH", "")
        env["FRONTEND_PORT"] = str(port)

        cmd = [
            python,
            "-m",
            "streamlit",
            "run",
            str(APP),
            "--server.port",
            str(port),
            "--server.address",
            "0.0.0.0",
            "--server.headless",
            "true",
            "--browser.serverAddress",
            "localhost",
        ]
        print(f"[INFO] Starting Streamlit on port {port}")
        try:
            popen_kwargs: dict[str, Any] = {"cwd": str(ROOT), "env": env}
            # On Windows, start in a new process group so Ctrl+C in parent doesn't kill child
            if os.name == "nt":
                popen_kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            self.proc = subprocess.Popen(cmd, **popen_kwargs)
            return True
        except (OSError, subprocess.SubprocessError) as e:
            print(f"[ERROR] Failed to start Streamlit: {e}")
            return False

    def is_running(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def stop(self, timeout: float = 5.0) -> None:
        if not self.proc:
            return
        try:
            if self.proc.poll() is None:
                self.proc.terminate()
                self.proc.wait(timeout=timeout)
                print("[CLEANUP] Frontend terminated")
        except subprocess.TimeoutExpired:
            print("[CLEANUP] Forcing frontend kill")
            try:
                self.proc.kill()
            except Exception:
                pass
        except Exception as e:
            print(f"[WARN] Frontend stop error: {e}")


class SmartStart:
    def __init__(self, port_range: Tuple[int, int] = DEFAULT_PORT_RANGE) -> None:
        self.port_range = port_range
        self.frontend = FrontendProcess()
        self._register_signals()

    def _register_signals(self) -> None:
        atexit.register(self.cleanup)
        try:
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
        except Exception:
            # On some platforms signals may not be available
            pass

    def _signal_handler(self, signum, frame) -> None:  # type: ignore[no-untyped-def]
        print(f"\n[INFO] Received signal {signum}, shutting down...")
        self.cleanup()
        sys.exit(0)

    def prepare_port(self) -> int:
        # Prefer last used port if still free
        state = _load_state()
        last = int(state.get("frontend_port", 0) or 0)
        if last and _is_port_free(last):
            print(f"[INFO] Reusing last free port: {last}")
            return last

        port = _find_free_port(self.port_range)
        if not port:
            raise RuntimeError(f"No free port found in range {self.port_range[0]}-{self.port_range[1]}")
        print(f"[INFO] Selected free port: {port}")
        return port

    def start_frontend(self) -> Tuple[bool, int]:
        port = self.prepare_port()
        ok = self.frontend.start(port)
        if not ok:
            return False, port

        # Readiness wait loop
        host = "127.0.0.1"
        url = f"http://{host}:{port}/"
        print(f"[INFO] Waiting for Streamlit readiness at {url} (timeout {READINESS_TIMEOUT_SEC}s)")
        started_at = time.time()
        attempts = 0
        while time.time() - started_at < READINESS_TIMEOUT_SEC:
            time.sleep(READINESS_POLL_INTERVAL_SEC)
            attempts += 1

            if not self.frontend.is_running():
                print("[ERROR] Frontend process exited prematurely")
                return False, port

            if _http_check(host, port, "/"):
                print(f"[SUCCESS] Frontend ready at {url}")
                _save_state({"frontend_port": port, "frontend_url": url})
                return True, port

            if attempts % 5 == 0:
                print(f"[INFO] Waiting for frontend... {attempts} attempts")

        print("[ERROR] Frontend readiness timed out")
        return False, port

    def check(self) -> bool:
        state = _load_state()
        port = int(state.get("frontend_port", 0) or 0)
        if not port:
            print("[CHECK] No previous frontend state found")
            return False
        ok = _http_check("127.0.0.1", port, "/")
        print(f"[CHECK] Frontend on {port}: {'UP' if ok else 'DOWN'}")
        return ok

    def cleanup(self) -> None:
        self.frontend.stop()
        _clear_state()


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Smart Start helper for Code2Graf with dynamic ports and health checks")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--app", action="store_true", help="Run Streamlit app UI (default)")
    g.add_argument("--cli", action="store_true", help="Run CLI main.py (passthrough)")
    p.add_argument("--check", action="store_true", help="Check current frontend health using last-known port")
    p.add_argument("--port-range", type=str, default=f"{DEFAULT_PORT_RANGE[0]}-{DEFAULT_PORT_RANGE[1]}",
                   help="Port range for frontend, e.g. 8501-8599")
    p.add_argument("--", dest="dashdash", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("args", nargs=argparse.REMAINDER, help="Arguments for CLI main.py (use -- to separate)")
    return p


def parse_port_range(spec: str) -> Tuple[int, int]:
    try:
        a, b = spec.split("-", 1)
        lo, hi = int(a), int(b)
        if lo > hi or lo <= 0:
            raise ValueError
        return lo, hi
    except Exception:
        raise argparse.ArgumentTypeError(f"Invalid --port-range: {spec}")


def run_cli_passthrough(extra_args: list[str]) -> int:
    main_py = ROOT / "main.py"
    if not main_py.exists():
        print(f"[ERROR] CLI entry not found at {main_py}")
        return 2
    extra = extra_args
    if extra and extra[0] == "--":
        extra = extra[1:]
    ensure_pythonpath()
    return run([sys.executable, str(main_py), *extra], cwd=ROOT, env=os.environ.copy())


def main() -> int:
    parser = build_arg_parser()
    ns = parser.parse_args()

    if ns.port_range:
        try:
            lo, hi = parse_port_range(ns.port_range)
        except argparse.ArgumentTypeError as e:
            print(f"[ERROR] {e}")
            return 2
    else:
        lo, hi = DEFAULT_PORT_RANGE

    if ns.check:
        mgr = SmartStart((lo, hi))
        return 0 if mgr.check() else 1

    if ns.cli:
        return run_cli_passthrough(ns.args)

    # Default to app mode
    ensure_pythonpath()
    if not APP.exists():
        print(f"[ERROR] Streamlit app not found at {APP}")
        return 2

    mgr = SmartStart((lo, hi))
    ok, _port = mgr.start_frontend()
    if not ok:
        return 1
    try:
        # Keep running until interrupted; graceful cleanup on exit
        while mgr.frontend.is_running():
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        mgr.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())