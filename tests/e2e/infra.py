"""
E2E Test Infrastructure for Vila Cachos AI (Opaque-Box, Non-Destructive).

Provides:
- Ephemeral port allocation (`127.0.0.1:0`)
- `CsvBackupGuard`: OS-level lock (`msvcrt.locking` in %TEMP%), SHA-256 verification,
  `atexit` + signal cleanup, strict teardown order (stop uvicorn tree BEFORE restoring CSV)
- `UvicornServer`: launches `api:app` with `--limit-concurrency 50` and `YOLO_REMOTE_URL=""`
- `ViteDevServer`: launches `npx vite dev` in `totem-ui/` with `VITE_API_URL` override
- `CdpBrowser`: pure-Python headless Chrome/Edge DevTools Protocol client via `websockets`
- `ReadOnlySuiteEnv` & `IsolatedFeedbackApiEnv`: clean isolation between read-only and
  CSV-mutating `/feedback` tests
- Synthetic & real image fixture builders
"""

from __future__ import annotations

import atexit
import hashlib
import io
import json
import msvcrt
import os
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import httpx
import psutil
from PIL import Image, ImageDraw
import websockets.sync.client as ws_sync

REPO_ROOT = Path(__file__).resolve().parents[2]
TOTEM_UI_DIR = REPO_ROOT / "totem-ui"
CSV_PATH = REPO_ROOT / "data" / "dataset_historico_vila_cachos.csv"

FIXTURE_HAIR_TIPO2 = REPO_ROOT / "dataset_cachos" / "val" / "tipo_2_ondulado" / "aug_000_base.jpg"
FIXTURE_HAIR_TIPO3 = REPO_ROOT / "dataset_cachos" / "val" / "tipo_3_cacheado" / "aug_000_base.jpg"
FIXTURE_HAIR_TIPO4 = REPO_ROOT / "dataset_cachos" / "val" / "tipo_4_crespo" / "aug_000_base.jpg"

EXPECTED_SECURITY_HEADERS = {
    "x-content-type-options": "nosniff",
    "x-frame-options": "DENY",
    "x-xss-protection": "1; mode=block",
    "referrer-policy": "strict-origin-when-cross-origin",
    "permissions-policy": "camera=(), microphone=(), geolocation=()",
}

_IP_LOCK = threading.Lock()
_IP_COUNTER = 0


def next_client_ip() -> str:
    """Return a unique synthetic IPv4 address for X-Forwarded-For SlowAPI isolation."""
    global _IP_COUNTER
    with _IP_LOCK:
        _IP_COUNTER += 1
        n = _IP_COUNTER
    b2 = (n >> 16) & 0xFF
    b3 = (n >> 8) & 0xFF
    b4 = (n & 0xFF) or 1
    return f"10.{b2}.{b3}.{b4}"


def ip_headers(ip: Optional[str] = None) -> Dict[str, str]:
    return {"X-Forwarded-For": ip or next_client_ip()}


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def kill_proc_tree(pid: int, timeout: float = 5.0) -> None:
    """Terminate a process and all its recursive descendants safely via psutil."""
    try:
        parent = psutil.Process(pid)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return

    children = []
    try:
        children = parent.children(recursive=True)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

    procs = children + [parent]
    for p in procs:
        try:
            p.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    _, alive = psutil.wait_procs(procs, timeout=timeout)
    for p in alive:
        try:
            p.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    if alive:
        psutil.wait_procs(alive, timeout=3.0)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


# Global registry of live managed processes for emergency cleanup on exit/signals
_ACTIVE_STOP_HOOKS: List[Callable[[], None]] = []
_HOOKS_LOCK = threading.Lock()


def _register_stop_hook(fn: Callable[[], None]) -> None:
    with _HOOKS_LOCK:
        if fn not in _ACTIVE_STOP_HOOKS:
            _ACTIVE_STOP_HOOKS.append(fn)


def _unregister_stop_hook(fn: Callable[[], None]) -> None:
    with _HOOKS_LOCK:
        if fn in _ACTIVE_STOP_HOOKS:
            _ACTIVE_STOP_HOOKS.remove(fn)


def stop_all_managed_processes() -> None:
    with _HOOKS_LOCK:
        hooks = list(_ACTIVE_STOP_HOOKS)
    for fn in reversed(hooks):
        try:
            fn()
        except Exception:
            pass


class CsvBackupGuard:
    """
    Non-destructive guard for `data/dataset_historico_vila_cachos.csv`.
    - Acquires an OS-level lock file in %TEMP% using `msvcrt.locking`.
    - Captures exact original bytes and SHA-256.
    - Writes crash-recovery backup in %TEMP%.
    - Registers `atexit` and signal cleanup.
    - Enforces strict teardown ordering: terminates all active `uvicorn` / managed
      process trees BEFORE restoring CSV bytes, then verifies SHA-256 equality.
    """

    _instance: Optional["CsvBackupGuard"] = None
    _inst_lock = threading.Lock()

    def __init__(self, csv_path: Path = CSV_PATH) -> None:
        self.csv_path = csv_path
        self.temp_dir = Path(tempfile.gettempdir())
        self.lock_path = self.temp_dir / "vila_cachos_e2e_csv.lock"
        self.bak_path = self.temp_dir / f"vila_cachos_csv_bak_{os.getpid()}.csv"
        self._lock_fh = None
        self._active = False
        self.original_bytes: bytes = b""
        self.original_sha256: str = ""
        self._cleanup_lock = threading.Lock()
        self._signals_installed = False

    @classmethod
    def acquire_global(cls) -> "CsvBackupGuard":
        with cls._inst_lock:
            if cls._instance is None:
                cls._instance = cls()
            if not cls._instance._active:
                cls._instance.enter()
            return cls._instance

    @classmethod
    def release_global(cls) -> None:
        with cls._inst_lock:
            if cls._instance is not None and cls._instance._active:
                cls._instance.exit()

    def _acquire_os_lock(self, timeout: float = 15.0) -> None:
        deadline = time.monotonic() + timeout
        fh = open(self.lock_path, "a+b")
        fh.seek(0, os.SEEK_END)
        if fh.tell() == 0:
            fh.write(b"1")
            fh.flush()
        fh.seek(0)

        while True:
            try:
                msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
                self._lock_fh = fh
                return
            except OSError:
                if time.monotonic() >= deadline:
                    fh.close()
                    raise TimeoutError(f"Could not acquire OS lock on {self.lock_path}")
                time.sleep(0.1)

    def _release_os_lock(self) -> None:
        if self._lock_fh is not None:
            try:
                self._lock_fh.seek(0)
                msvcrt.locking(self._lock_fh.fileno(), msvcrt.LK_UNLCK, 1)
            except OSError:
                pass
            try:
                self._lock_fh.close()
            except OSError:
                pass
            self._lock_fh = None
        try:
            if self.lock_path.exists():
                self.lock_path.unlink()
        except OSError:
            pass

    def enter(self) -> "CsvBackupGuard":
        with self._cleanup_lock:
            if self._active:
                return self
            self._acquire_os_lock()
            self.original_bytes = self.csv_path.read_bytes()
            self.original_sha256 = sha256_bytes(self.original_bytes)
            self.bak_path.write_bytes(self.original_bytes)
            self._active = True
            if not self._signals_installed:
                atexit.register(self._atexit_cleanup)
                self._install_signal_handlers()
                self._signals_installed = True
            return self

    def restore_csv(self, stop_servers_first: bool = False) -> str:
        """
        Restore CSV bytes and verify SHA-256 matches original.
        If `stop_servers_first=True`, stops all managed servers before writing.
        """
        if stop_servers_first:
            stop_all_managed_processes()

        if not self._active or not self.original_bytes:
            return self.original_sha256

        last_err: Optional[Exception] = None
        for _ in range(30):
            try:
                with open(self.csv_path, "wb") as f:
                    f.write(self.original_bytes)
                    f.flush()
                    os.fsync(f.fileno())
                last_err = None
                break
            except PermissionError as exc:
                last_err = exc
                time.sleep(0.1)
        if last_err is not None:
            raise last_err

        restored_sha = sha256_file(self.csv_path)
        if restored_sha != self.original_sha256:
            raise RuntimeError(
                f"CSV SHA-256 mismatch after restore! expected={self.original_sha256} actual={restored_sha}"
            )
        return restored_sha

    def exit(self) -> None:
        with self._cleanup_lock:
            if not self._active:
                return
            try:
                # Strict teardown order: stop all uvicorn/vite/chrome trees BEFORE restoring CSV
                stop_all_managed_processes()
                self.restore_csv(stop_servers_first=False)
            finally:
                try:
                    if self.bak_path.exists():
                        self.bak_path.unlink()
                except OSError:
                    pass
                self._release_os_lock()
                self._active = False

    def _atexit_cleanup(self) -> None:
        try:
            self.exit()
        except Exception:
            pass

    def _install_signal_handlers(self) -> None:
        def _handler(signum, frame):
            try:
                self.exit()
            finally:
                signal.signal(signum, signal.SIG_DFL)
                os.kill(os.getpid(), signum)

        for sig_name in ("SIGINT", "SIGTERM", "SIGBREAK"):
            sig = getattr(signal, sig_name, None)
            if sig is not None:
                try:
                    signal.signal(sig, _handler)
                except (ValueError, OSError):
                    pass

    def __enter__(self) -> "CsvBackupGuard":
        return self.enter()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.exit()


class UvicornServer:
    """Ephemeral local Uvicorn server on `127.0.0.1:<free_port>`."""

    def __init__(self, port: Optional[int] = None) -> None:
        self.port = port or get_free_port()
        self.base_url = f"http://127.0.0.1:{self.port}"
        self.proc: Optional[subprocess.Popen] = None
        self._log_file = None
        self._log_path: Optional[Path] = None

    def start(self, timeout: float = 45.0) -> "UvicornServer":
        if self.proc is not None:
            return self
        CsvBackupGuard.acquire_global()

        fd, log_name = tempfile.mkstemp(prefix=f"uvicorn_e2e_{self.port}_", suffix=".log")
        os.close(fd)
        self._log_path = Path(log_name)
        self._log_file = open(self._log_path, "wb")

        env = os.environ.copy()
        env["YOLO_REMOTE_URL"] = ""
        env["PYTHONUNBUFFERED"] = "1"

        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "api:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(self.port),
            "--limit-concurrency",
            "50",
            "--log-level",
            "warning",
        ]
        self.proc = subprocess.Popen(
            cmd,
            cwd=str(REPO_ROOT),
            env=env,
            stdout=self._log_file,
            stderr=subprocess.STDOUT,
        )
        _register_stop_hook(self.stop)

        deadline = time.monotonic() + timeout
        last_err = ""
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                log_txt = self._read_log()
                self.stop()
                raise RuntimeError(f"Uvicorn exited prematurely (rc={self.proc.returncode if self.proc else '?'})\n{log_txt}")
            try:
                r = httpx.get(f"{self.base_url}/health", timeout=2.0)
                if r.status_code == 200:
                    return self
                last_err = f"HTTP {r.status_code}"
            except Exception as exc:
                last_err = str(exc)
            time.sleep(0.25)

        log_txt = self._read_log()
        self.stop()
        raise TimeoutError(f"Uvicorn failed to become healthy on {self.base_url} ({last_err})\n{log_txt}")

    def _read_log(self) -> str:
        if self._log_path and self._log_path.exists():
            try:
                return self._log_path.read_text(encoding="utf-8", errors="replace")[-3000:]
            except Exception:
                return ""
        return ""

    def memory_stats_mb(self) -> Dict[str, float]:
        if self.proc is None:
            raise RuntimeError("UvicornServer not running")
        p = psutil.Process(self.proc.pid)
        mi = p.memory_info()
        rss_mb = mi.rss / (1024 * 1024)
        peak_wset_mb = getattr(mi, "peak_wset", mi.rss) / (1024 * 1024)
        handles = p.num_handles() if hasattr(p, "num_handles") else 0
        return {
            "rss_mb": rss_mb,
            "peak_wset_mb": peak_wset_mb,
            "handles": float(handles),
        }

    def stop(self) -> None:
        _unregister_stop_hook(self.stop)
        if self.proc is not None:
            kill_proc_tree(self.proc.pid)
            self.proc = None
        if self._log_file is not None:
            try:
                self._log_file.close()
            except Exception:
                pass
            self._log_file = None
        if self._log_path and self._log_path.exists():
            try:
                self._log_path.unlink()
            except OSError:
                pass
            self._log_path = None


class ViteDevServer:
    """Ephemeral `vite dev` server in `totem-ui/` bound to `127.0.0.1:<free_port>`."""

    def __init__(self, api_url: str, port: Optional[int] = None) -> None:
        self.api_url = api_url
        self.port = port or get_free_port()
        self.base_url = f"http://127.0.0.1:{self.port}"
        self.proc: Optional[subprocess.Popen] = None
        self._log_file = None
        self._log_path: Optional[Path] = None

    def start(self, timeout: float = 60.0) -> "ViteDevServer":
        if self.proc is not None:
            return self

        fd, log_name = tempfile.mkstemp(prefix=f"vite_e2e_{self.port}_", suffix=".log")
        os.close(fd)
        self._log_path = Path(log_name)
        self._log_file = open(self._log_path, "wb")

        env = os.environ.copy()
        env["VITE_API_URL"] = self.api_url
        env["BROWSER"] = "none"

        cmd = [
            "cmd",
            "/c",
            "npx",
            "vite",
            "dev",
            "--host",
            "127.0.0.1",
            "--port",
            str(self.port),
            "--strictPort",
        ]
        self.proc = subprocess.Popen(
            cmd,
            cwd=str(TOTEM_UI_DIR),
            env=env,
            stdout=self._log_file,
            stderr=subprocess.STDOUT,
        )
        _register_stop_hook(self.stop)

        deadline = time.monotonic() + timeout
        last_err = ""
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                log_txt = self._read_log()
                self.stop()
                raise RuntimeError(f"Vite exited prematurely\n{log_txt}")
            try:
                r = httpx.get(f"{self.base_url}/", timeout=3.0)
                if r.status_code == 200 and len(r.text) > 500:
                    # Warm up /admin route SSR/transform so first browser navigation is fast
                    try:
                        httpx.get(f"{self.base_url}/admin", timeout=10.0)
                    except Exception:
                        pass
                    return self
                last_err = f"HTTP {r.status_code}"
            except Exception as exc:
                last_err = str(exc)
            time.sleep(0.35)

        log_txt = self._read_log()
        self.stop()
        raise TimeoutError(f"Vite failed to become ready on {self.base_url} ({last_err})\n{log_txt}")

    def _read_log(self) -> str:
        if self._log_path and self._log_path.exists():
            try:
                return self._log_path.read_text(encoding="utf-8", errors="replace")[-3000:]
            except Exception:
                return ""
        return ""

    def stop(self) -> None:
        _unregister_stop_hook(self.stop)
        if self.proc is not None:
            kill_proc_tree(self.proc.pid)
            self.proc = None
        if self._log_file is not None:
            try:
                self._log_file.close()
            except Exception:
                pass
            self._log_file = None
        if self._log_path and self._log_path.exists():
            try:
                self._log_path.unlink()
            except OSError:
                pass
            self._log_path = None


def find_browser_executable() -> str:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    raise FileNotFoundError("Neither Chrome nor Edge executable found on Windows.")


class CdpBrowser:
    """
    Pure-Python Chrome/Edge DevTools Protocol (CDP) headless browser driver over `websockets`.
    Supports navigation, JS evaluation, waiting, button clicking, React input typing,
    file upload (`DOM.setFileInputFiles`), viewport emulation, console/exception/network capture,
    and lazy-image scroll+decode verification.
    """

    def __init__(self) -> None:
        self.cdp_port = get_free_port()
        self.proc: Optional[subprocess.Popen] = None
        self.user_data_dir: Optional[Path] = None
        self.ws = None
        self._msg_id = 0
        self.console_errors: List[str] = []
        self.page_exceptions: List[str] = []
        self.network_responses: List[Dict[str, Any]] = []
        self.network_requests: List[Dict[str, Any]] = []
        self._req_id_to_url: Dict[str, str] = {}

    def start(self, timeout: float = 25.0) -> "CdpBrowser":
        if self.ws is not None:
            return self
        exe = find_browser_executable()
        self.user_data_dir = Path(tempfile.mkdtemp(prefix="vila_cachos_cdp_"))
        cmd = [
            exe,
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-dev-shm-usage",
            "--disable-extensions",
            "--window-size=1440,900",
            f"--remote-debugging-port={self.cdp_port}",
            f"--user-data-dir={self.user_data_dir}",
            "about:blank",
        ]
        self.proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _register_stop_hook(self.stop)

        ws_url = None
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                r = httpx.get(f"http://127.0.0.1:{self.cdp_port}/json", timeout=2.0)
                if r.status_code == 200:
                    targets = r.json()
                    for t in targets:
                        if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                            ws_url = t["webSocketDebuggerUrl"]
                            break
                if ws_url:
                    break
            except Exception:
                pass
            time.sleep(0.2)

        if not ws_url:
            self.stop()
            raise TimeoutError("Timed out waiting for Chrome/Edge CDP WebSocket URL")

        self.ws = ws_sync.connect(ws_url, max_size=20 * 1024 * 1024)
        self.send("Page.enable")
        self.send("Runtime.enable")
        self.send("DOM.enable")
        self.send("Network.enable")
        return self

    def _record_event(self, evt: Dict[str, Any]) -> None:
        method = evt.get("method", "")
        params = evt.get("params", {})
        if method == "Runtime.consoleAPICalled":
            if params.get("type") == "error":
                args = params.get("args", [])
                msg = " ".join(str(a.get("value") or a.get("description") or "") for a in args)
                self.console_errors.append(msg)
        elif method == "Runtime.exceptionThrown":
            details = params.get("exceptionDetails", {})
            text = details.get("text", "")
            exc = details.get("exception", {}).get("description", "")
            self.page_exceptions.append(f"{text} {exc}".strip())
        elif method == "Network.requestWillBeSent":
            req = params.get("request", {})
            req_id = params.get("requestId", "")
            url = req.get("url", "")
            if req_id:
                self._req_id_to_url[req_id] = url
            self.network_requests.append(
                {"url": url, "method": req.get("method", ""), "type": params.get("type", "")}
            )
        elif method == "Network.responseReceived":
            resp = params.get("response", {})
            self.network_responses.append(
                {
                    "url": resp.get("url", ""),
                    "status": resp.get("status", 0),
                    "mimeType": resp.get("mimeType", ""),
                    "type": params.get("type", ""),
                }
            )

    def send(self, method: str, params: Optional[Dict[str, Any]] = None, timeout: float = 20.0) -> Dict[str, Any]:
        if self.ws is None:
            raise RuntimeError("CdpBrowser not started")
        self._msg_id += 1
        cid = self._msg_id
        payload = {"id": cid, "method": method, "params": params or {}}
        self.ws.send(json.dumps(payload))

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            raw = self.ws.recv(timeout=max(0.2, deadline - time.monotonic()))
            msg = json.loads(raw)
            if "id" in msg and msg["id"] == cid:
                if "error" in msg:
                    raise RuntimeError(f"CDP error in {method}: {msg['error']}")
                return msg.get("result", {})
            if "method" in msg:
                self._record_event(msg)
        raise TimeoutError(f"CDP timeout waiting for {method}")

    def drain_events(self, wait_sec: float = 0.05) -> None:
        if self.ws is None:
            return
        deadline = time.monotonic() + wait_sec
        while time.monotonic() < deadline:
            try:
                raw = self.ws.recv(timeout=0.02)
                msg = json.loads(raw)
                if "method" in msg:
                    self._record_event(msg)
            except TimeoutError:
                break
            except Exception:
                break

    def reset_logs(self) -> None:
        self.drain_events(0.05)
        self.console_errors.clear()
        self.page_exceptions.clear()
        self.network_responses.clear()
        self.network_requests.clear()

    def set_viewport(self, width: int, height: int, mobile: bool = False) -> None:
        self.send(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": width,
                "height": height,
                "deviceScaleFactor": 2 if mobile else 1,
                "mobile": mobile,
            },
        )

    def reset_viewport(self) -> None:
        self.set_viewport(1440, 900, mobile=False)

    def eval_js(self, expr: str, await_promise: bool = True) -> Any:
        res = self.send(
            "Runtime.evaluate",
            {
                "expression": expr,
                "returnByValue": True,
                "awaitPromise": await_promise,
            },
        )
        if "exceptionDetails" in res:
            details = res["exceptionDetails"]
            raise RuntimeError(f"JS eval exception: {details}")
        obj = res.get("result", {})
        return obj.get("value")

    def wait_for_hydrated(self, timeout: float = 15.0) -> None:
        """Wait until React client hydration has attached event/fiber handlers in the DOM."""
        self.wait_for(
            """
            (() => {
                const els = document.querySelectorAll('button, a, main, section');
                for (const el of els) {
                    const keys = Object.keys(el);
                    if (keys.some(k => k.startsWith('__reactFiber$') || k.startsWith('__reactProps$'))) {
                        return true;
                    }
                }
                return false;
            })()
            """,
            timeout=timeout,
        )

    def navigate(self, url: str, wait_ready: bool = True, wait_hydrated: bool = True, timeout: float = 20.0) -> None:
        self.send("Page.navigate", {"url": url})
        if wait_ready:
            self.wait_for("document.readyState === 'complete'", timeout=timeout)
            if wait_hydrated:
                self.wait_for_hydrated(timeout=timeout)
            time.sleep(0.15)
            self.drain_events(0.1)

    def wait_for(self, js_condition: str, timeout: float = 15.0, interval: float = 0.15) -> None:
        deadline = time.monotonic() + timeout
        last_exc = None
        while time.monotonic() < deadline:
            try:
                if self.eval_js(f"Boolean({js_condition})"):
                    self.drain_events(0.03)
                    return
            except Exception as exc:
                last_exc = exc
            time.sleep(interval)
        body_snippet = ""
        try:
            body_snippet = str(self.eval_js("document.body ? document.body.innerText.slice(0, 600) : ''"))
        except Exception:
            pass
        raise TimeoutError(
            f"Timeout ({timeout}s) waiting for condition: {js_condition}\nLast err: {last_exc}\nBody: {body_snippet}"
        )

    def wait_for_text(self, text: str, timeout: float = 15.0, case_sensitive: bool = False) -> None:
        lit = json.dumps(text if case_sensitive else text.lower())
        if case_sensitive:
            self.wait_for(
                f"document.body && document.body.innerText.includes({lit})",
                timeout=timeout,
            )
        else:
            self.wait_for(
                f"document.body && document.body.innerText.toLowerCase().includes({lit})",
                timeout=timeout,
            )

    def body_text(self) -> str:
        return str(self.eval_js("document.body ? document.body.innerText : ''") or "")

    def click_button(self, text_substr: str, exact: bool = False, timeout: float = 10.0) -> None:
        lit = json.dumps(text_substr)
        exact_js = "true" if exact else "false"
        find_js = f"""
        (() => {{
            const needle = {lit};
            const exact = {exact_js};
            const btns = Array.from(document.querySelectorAll('button, a'));
            const el = btns.find(b => {{
                const t = (b.innerText || b.textContent || '').replace(/\\s+/g, ' ').trim();
                const aria = (b.getAttribute('aria-label') || '').trim();
                if (exact) return t === needle || aria === needle;
                return t.includes(needle) || aria.includes(needle);
            }});
            if (!el) return null;
            if (el.disabled) return 'DISABLED';
            el.scrollIntoView({{ block: 'center' }});
            el.click();
            return 'CLICKED';
        }})()
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            status = self.eval_js(find_js)
            if status == "CLICKED":
                self.drain_events(0.05)
                return
            time.sleep(0.12)
        raise TimeoutError(f"Could not click button matching {text_substr!r} (exact={exact})")

    def is_button_disabled(self, text_substr: str) -> bool:
        lit = json.dumps(text_substr)
        return bool(
            self.eval_js(
                f"""
                (() => {{
                    const btns = Array.from(document.querySelectorAll('button'));
                    const el = btns.find(b => (b.innerText || '').replace(/\\s+/g, ' ').trim().includes({lit}));
                    if (!el) throw new Error('Button not found: ' + {lit});
                    return Boolean(el.disabled);
                }})()
                """
            )
        )

    def click_selector(self, selector: str) -> None:
        lit = json.dumps(selector)
        ok = self.eval_js(
            f"""
            (() => {{
                const el = document.querySelector({lit});
                if (!el) return false;
                el.scrollIntoView({{ block: 'center' }});
                el.click();
                return true;
            }})()
            """
        )
        if not ok:
            raise AssertionError(f"Selector not found for click: {selector}")
        self.drain_events(0.05)

    def set_input_value(self, selector: str, value: str) -> None:
        sel_lit = json.dumps(selector)
        val_lit = json.dumps(value)
        ok = self.eval_js(
            f"""
            (() => {{
                const el = document.querySelector({sel_lit});
                if (!el) return false;
                el.scrollIntoView({{ block: 'center' }});
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(el, {val_lit});
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return true;
            }})()
            """
        )
        if not ok:
            raise AssertionError(f"Input selector not found: {selector}")
        self.drain_events(0.05)

    def upload_file(self, selector: str, file_path: Path) -> None:
        resolved = str(Path(file_path).resolve())
        doc = self.send("DOM.getDocument", {"depth": -1})
        root_id = doc["root"]["nodeId"]
        node = self.send("DOM.querySelector", {"nodeId": root_id, "selector": selector})
        node_id = node.get("nodeId", 0)
        if not node_id:
            raise AssertionError(f"File input selector not found: {selector}")
        self.send("DOM.setFileInputFiles", {"nodeId": node_id, "files": [resolved]})
        self.drain_events(0.1)

    def press_escape(self) -> None:
        self.send(
            "Input.dispatchKeyEvent",
            {
                "type": "keyDown",
                "key": "Escape",
                "code": "Escape",
                "windowsVirtualKeyCode": 27,
                "nativeVirtualKeyCode": 27,
            },
        )
        self.send(
            "Input.dispatchKeyEvent",
            {
                "type": "keyUp",
                "key": "Escape",
                "code": "Escape",
                "windowsVirtualKeyCode": 27,
                "nativeVirtualKeyCode": 27,
            },
        )
        self.drain_events(0.05)

    def verify_images_loaded(self, selector: str = "img", min_count: int = 1, timeout_per_img: float = 5.0) -> List[Dict[str, Any]]:
        sel_lit = json.dumps(selector)
        count = int(self.eval_js(f"document.querySelectorAll({sel_lit}).length") or 0)
        if count < min_count:
            raise AssertionError(f"Expected >= {min_count} images for '{selector}', found {count}")

        results: List[Dict[str, Any]] = []
        for idx in range(count):
            self.eval_js(
                f"""
                (() => {{
                    const imgs = document.querySelectorAll({sel_lit});
                    if (imgs[{idx}]) imgs[{idx}].scrollIntoView({{ block: 'center' }});
                }})()
                """
            )
            deadline = time.monotonic() + timeout_per_img
            info = None
            while time.monotonic() < deadline:
                info = self.eval_js(
                    f"""
                    (() => {{
                        const img = document.querySelectorAll({sel_lit})[{idx}];
                        if (!img) return null;
                        return {{
                            alt: img.alt || '',
                            src: img.currentSrc || img.src || '',
                            complete: Boolean(img.complete),
                            naturalWidth: Number(img.naturalWidth || 0)
                        }};
                    }})()
                    """
                )
                if info and info["complete"] and info["naturalWidth"] > 0:
                    break
                time.sleep(0.08)
            results.append(info or {"alt": "", "src": "", "complete": False, "naturalWidth": 0})
        return results

    def horizontal_overflow_px(self) -> int:
        val = self.eval_js(
            "Math.max(0, document.documentElement.scrollWidth - window.innerWidth)"
        )
        return int(val or 0)

    def stop(self) -> None:
        _unregister_stop_hook(self.stop)
        if self.ws is not None:
            try:
                self.ws.close()
            except Exception:
                pass
            self.ws = None
        if self.proc is not None:
            kill_proc_tree(self.proc.pid)
            self.proc = None
        if self.user_data_dir and self.user_data_dir.exists():
            shutil.rmtree(self.user_data_dir, ignore_errors=True)
            self.user_data_dir = None


class ReadOnlySuiteEnv:
    """
    Shared read-only runtime environment (`UvicornServer` + `ViteDevServer` + `CdpBrowser`).
    NEVER receives `POST /feedback`, ensuring `data/dataset_historico_vila_cachos.csv`
    and `total_clientes_historico` stay pristine across all read-only tests.
    """

    _api: Optional[UvicornServer] = None
    _ui: Optional[ViteDevServer] = None
    _browser: Optional[CdpBrowser] = None
    _lock = threading.Lock()

    @classmethod
    def api(cls) -> UvicornServer:
        with cls._lock:
            if cls._api is None or cls._api.proc is None:
                cls._api = UvicornServer().start()
            return cls._api

    @classmethod
    def ui(cls) -> ViteDevServer:
        api = cls.api()
        with cls._lock:
            if cls._ui is None or cls._ui.proc is None:
                cls._ui = ViteDevServer(api_url=api.base_url).start()
            return cls._ui

    @classmethod
    def browser(cls) -> CdpBrowser:
        with cls._lock:
            if cls._browser is None or cls._browser.ws is None:
                cls._browser = CdpBrowser().start()
            return cls._browser

    @classmethod
    def shutdown(cls) -> None:
        with cls._lock:
            if cls._browser is not None:
                cls._browser.stop()
                cls._browser = None
            if cls._ui is not None:
                cls._ui.stop()
                cls._ui = None
            if cls._api is not None:
                cls._api.stop()
                cls._api = None


class IsolatedFeedbackApiEnv:
    """
    Context manager / class helper for tests that call `POST /feedback`.
    Starts a dedicated `UvicornServer`, yields it, and on teardown:
    1. Terminates the dedicated `UvicornServer` process tree FIRST.
    2. Restores `data/dataset_historico_vila_cachos.csv` bytes via `CsvBackupGuard`
       and verifies SHA-256 matches the original dataset.
    """

    def __init__(self) -> None:
        self.guard = CsvBackupGuard.acquire_global()
        self.server: Optional[UvicornServer] = None

    def start(self) -> UvicornServer:
        self.server = UvicornServer().start()
        return self.server

    def stop_and_restore(self) -> str:
        if self.server is not None:
            self.server.stop()
            self.server = None
        return self.guard.restore_csv(stop_servers_first=False)

    def __enter__(self) -> UvicornServer:
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop_and_restore()


# ---------------------------------------------------------------------------
# Synthetic & Real Image Fixture Helpers
# ---------------------------------------------------------------------------

def load_hair_image_bytes(curvature: int = 3, fmt: str = "JPEG", resize_to: Optional[tuple] = None) -> bytes:
    src_map = {
        2: FIXTURE_HAIR_TIPO2,
        3: FIXTURE_HAIR_TIPO3,
        4: FIXTURE_HAIR_TIPO4,
    }
    src = src_map.get(curvature, FIXTURE_HAIR_TIPO3)
    if fmt.upper() == "JPEG" and resize_to is None:
        return src.read_bytes()

    with Image.open(src) as img:
        rgb = img.convert("RGB")
        if resize_to is not None:
            rgb = rgb.resize(resize_to, Image.Resampling.BILINEAR)
        buf = io.BytesIO()
        rgb.save(buf, format=fmt.upper(), quality=90)
        return buf.getvalue()


def make_non_hair_skin_jpeg(width: int = 400, height: int = 400) -> bytes:
    """Uniform warm skin-tone JPEG (triggers non-hair skin/bald rejection)."""
    img = Image.new("RGB", (width, height), (214, 166, 134))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    return buf.getvalue()


def make_non_hair_banner_jpeg(width: int = 600, height: int = 400) -> bytes:
    """Blue graphic banner with high-contrast rectangles/lines (non-hair graphic)."""
    img = Image.new("RGB", (width, height), (25, 85, 210))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 560, 140], fill=(245, 245, 245))
    draw.rectangle([40, 180, 560, 340], fill=(15, 45, 130), outline=(255, 220, 50), width=6)
    draw.text((80, 75), "PROMO VILA CACHOS 50% OFF", fill=(20, 20, 20))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    return buf.getvalue()


def make_non_hair_grid_jpeg(width: int = 500, height: int = 500) -> bytes:
    """White document/grid image (non-hair document rejection)."""
    img = Image.new("RGB", (width, height), (252, 252, 252))
    draw = ImageDraw.Draw(img)
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(40, 40, 40), width=2)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(40, 40, 40), width=2)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def make_large_uniform_jpeg(width: int, height: int) -> bytes:
    img = Image.new("RGB", (width, height), (190, 150, 120))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=75)
    return buf.getvalue()


def write_temp_file(data: bytes, suffix: str = ".jpg") -> Path:
    fd, path = tempfile.mkstemp(prefix="vc_e2e_img_", suffix=suffix)
    os.close(fd)
    p = Path(path)
    p.write_bytes(data)
    return p
