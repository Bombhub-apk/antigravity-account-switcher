#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatGPT Desktop & Codex Chrome DevTools Protocol (CDP) Injector Daemon
Connects to ChatGPT Desktop instances and injects Persian fonts, themes, and HUD action pill.
Works for both outer Electron pages and inner chat webviews.
"""

import os
import sys
import json
import time
import asyncio
import logging
import urllib.request
from pathlib import Path

try:
    import websockets
except ImportError:
    websockets = None

CURRENT_DIR = Path(__file__).resolve().parent
INJECTOR_JS_PATH = CURRENT_DIR / "chatgpt_theme_injector.js"
LOG_FILE = CURRENT_DIR / "chatgpt_cdp_daemon.log"
handlers = [logging.FileHandler(LOG_FILE, encoding="utf-8")]
if sys.stdout is not None:
    handlers.append(logging.StreamHandler(sys.stdout))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=handlers
)
logger = logging.getLogger("chatgpt_cdp")

def load_injector_script():
    if not INJECTOR_JS_PATH.exists():
        return ""
    try:
        header = ""
        try:
            import chatgpt_account_manager as cpm
            profiles = cpm.list_profiles()
            settings = cpm.load_settings()
            init_data = json.dumps({"profiles": profiles, "settings": settings}, ensure_ascii=False)
            header = f"window.__cpe_initial_data = {init_data};\n"
        except Exception:
            pass

        with open(INJECTOR_JS_PATH, "r", encoding="utf-8") as f:
            return header + f.read()
    except Exception as e:
        logger.error(f"Failed to read injector script: {e}")
        return ""

def get_candidate_hosts(port):
    """Returns candidate IPs to probe for DevTools on Windows and POSIX."""
    hosts = ["127.0.0.1", "localhost"]
    try:
        import socket
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if ip not in hosts:
                hosts.append(ip)
    except Exception:
        pass
    try:
        import psutil
        for conn in psutil.net_connections(kind='tcp'):
            if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
                ip = conn.laddr.ip
                if ip and ip not in ("0.0.0.0", "::") and ip not in hosts:
                    hosts.insert(0, ip)
    except Exception:
        pass
    return hosts

def get_open_targets(port):
    """Fetches list of debuggable targets from Chromium DevTools port across candidate interfaces."""
    for host in get_candidate_hosts(port):
        url = f"http://{host}:{port}/json/list"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ChatGPT-Enhanced-Daemon"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if isinstance(data, list) and data:
                    return data
        except Exception:
            pass
    return []

def is_valid_chatgpt_target(t):
    """Checks whether a target is a valid ChatGPT surface (page, app, webview, or embedded frame)."""
    ws_url = t.get("webSocketDebuggerUrl")
    if not ws_url:
        return False
    t_type = t.get("type", "")
    t_url = (t.get("url") or "").lower()
    t_title = (t.get("title") or "").lower()

    # Reject internal chrome extensions or devtools panels
    if any(x in t_url for x in ["devtools://", "chrome-extension://"]):
        return False

    # Accept any surface hosting chatgpt.com or openai.com
    if "chatgpt.com" in t_url or "openai.com" in t_url:
        return True

    # For app/page/webview/other surfaces
    if t_type in ("page", "app", "webview", "other"):
        return any(x in (t_url + " " + t_title) for x in ["chatgpt", "codex", "app://"])

    return False

async def send_cdp_cmd(ws, msg_id, method, params, timeout=8.0):
    await ws.send(json.dumps({"id": msg_id, "method": method, "params": params}))
    start_t = time.time()
    while time.time() - start_t < timeout:
        remaining = timeout - (time.time() - start_t)
        if remaining <= 0:
            break
        try:
            raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
            data = json.loads(raw)
            if data.get("id") == msg_id:
                return data
        except asyncio.TimeoutError:
            break
    return None

async def handle_target_ipc(ws, raw_msg):
    """Handles bidirectional native IPC calls from ChatGPT webview, bypassing CSP completely."""
    try:
        msg = json.loads(raw_msg)
        if msg.get("method") == "Runtime.bindingCalled" and msg.get("params", {}).get("name") == "__cpe_daemon_ipc":
            payload_str = msg["params"].get("payload", "{}")
            payload = json.loads(payload_str)
            req_id = payload.get("id")
            action = payload.get("action")
            import chatgpt_account_manager as cpm
            resp = {}

            if action == "login":
                mode = payload.get("mode", "oauth")
                api_key = payload.get("api_key")
                ok, res = cpm.trigger_codex_login(mode=mode, api_key=api_key)
                if isinstance(res, dict):
                    resp = {"success": ok, "auth_url": res.get("auth_url"), "message": res.get("message", "")}
                else:
                    resp = {"success": ok, "message": str(res)}

            elif action in ("status", "get_status"):
                profiles = cpm.list_profiles()
                settings = cpm.load_settings()
                resp = {"status": "ok", "profiles": profiles, "settings": settings}

            elif action == "switch":
                prof_id = payload.get("profile_id")
                ok, res = cpm.switch_profile(prof_id)
                resp = {"success": ok, "message": res}

            elif action == "save_profile":
                prof_id = payload.get("profile_id")
                name = payload.get("name")
                ok, res = cpm.save_current_profile(prof_id, display_name=name)
                resp = {"success": ok, "profile": res}

            elif action == "save_settings":
                ok, res = cpm.save_settings(payload.get("settings", {}))
                resp = {"success": ok, "settings": res}

            elif action == "logout":
                ok, res = cpm.trigger_codex_logout()
                resp = {"success": ok, "message": res}

            elif action == "launch":
                inst = int(payload.get("instance", 1))
                new_win = bool(payload.get("new_window", False))
                ok, res = cpm.launch_chatgpt(instance_num=inst, new_window=new_win)
                resp = {"success": ok, "message": res}

            # Reply to the webview
            reply_code = f"window.__cpe_on_ipc_reply && window.__cpe_on_ipc_reply({json.dumps(req_id)}, {json.dumps(resp, ensure_ascii=False)});"
            await ws.send(json.dumps({
                "id": int(time.time() * 1000) % 1000000,
                "method": "Runtime.evaluate",
                "params": {"expression": reply_code}
            }))
    except Exception as e:
        logger.error(f"Error handling CPE IPC: {e}")

async def target_worker(t_id, ws_url):
    """Dedicated persistent worker for an active ChatGPT DevTools target."""
    while True:
        try:
            async with websockets.connect(ws_url, ping_interval=15, ping_timeout=10, close_timeout=3) as ws:
                logger.info(f"[CPE WORKER] Connected to target {t_id}")
                # Enable Runtime domain so bindingCalled events are delivered
                await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
                await ws.send(json.dumps({"id": 2, "method": "Runtime.addBinding", "params": {"name": "__cpe_daemon_ipc"}}))
                try:
                    await asyncio.wait_for(ws.recv(), timeout=2.0)
                except Exception:
                    pass

                # Inject script
                script = load_injector_script()
                if script:
                    await ws.send(json.dumps({
                        "id": 3,
                        "method": "Runtime.evaluate",
                        "params": {"expression": script, "userGesture": True}
                    }))
                    try:
                        await asyncio.wait_for(ws.recv(), timeout=4.0)
                    except Exception:
                        pass

                # Listen for IPC messages
                async for raw in ws:
                    await handle_target_ipc(ws, raw)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.debug(f"[CPE WORKER] Worker error for {t_id}: {e}")
            await asyncio.sleep(2.0)

async def check_and_inject_target(ws_url, script, force=False):
    """Connects via WebSocket, binds IPC, and injects if needed."""
    if not websockets or not ws_url or not script:
        return False
    try:
        async with websockets.connect(ws_url, ping_interval=None, ping_timeout=8, close_timeout=3) as ws:
            # Bind native IPC
            await ws.send(json.dumps({"id": 9, "method": "Runtime.enable"}))
            await ws.send(json.dumps({"id": 10, "method": "Runtime.addBinding", "params": {"name": "__cpe_daemon_ipc"}}))
            try:
                await asyncio.wait_for(ws.recv(), timeout=2.0)
            except Exception:
                pass

            if not force:
                check_resp = await send_cdp_cmd(ws, 1, "Runtime.evaluate", {
                    "expression": "Boolean(document.getElementById('cpe-hud-pill'))",
                    "returnByValue": True
                }, timeout=3.0)
                has_pill = check_resp.get("result", {}).get("result", {}).get("value") if check_resp else False
                if has_pill:
                    return False

            # Inject the suite
            eval_resp = await send_cdp_cmd(ws, 2, "Runtime.evaluate", {
                "expression": script,
                "returnByValue": True,
                "userGesture": True
            }, timeout=8.0)
            if eval_resp and "exceptionDetails" in eval_resp.get("result", {}):
                ex = eval_resp["result"]["exceptionDetails"]
                logger.error(f"Injection failed with exception on {ws_url[:40]}: {ex.get('text', '')} - {ex.get('exception', {}).get('description', '')}")
                return False

            logger.info(f"Enhanced suite successfully injected into: {ws_url[:50]}...")
            return True
    except Exception as e:
        logger.debug(f"Target WebSocket error for {ws_url}: {e}")
        return False

async def scan_and_inject_once(ports=[9223, 9224], force=False):
    script = load_injector_script()
    if not script:
        return 0

    success_count = 0
    for port in ports:
        targets = get_open_targets(port)
        for t in targets:
            if is_valid_chatgpt_target(t):
                ws_url = t.get("webSocketDebuggerUrl")
                ok = await check_and_inject_target(ws_url, script, force=force)
                if ok:
                    success_count += 1
    return success_count

async def daemon_loop(ports=[9223, 9224], poll_interval=2.0):
    logger.info(f"ChatGPT CDP Injector Daemon active on ports {ports}")
    workers = {}  # t_id -> asyncio.Task
    while True:
        try:
            current_target_ids = set()
            for port in ports:
                targets = get_open_targets(port)
                for t in targets:
                    if is_valid_chatgpt_target(t):
                        t_id = t.get("id") or t.get("webSocketDebuggerUrl")
                        ws_url = t.get("webSocketDebuggerUrl")
                        current_target_ids.add(t_id)
                        if t_id not in workers or workers[t_id].done():
                            workers[t_id] = asyncio.create_task(target_worker(t_id, ws_url))

            # Cancel workers for closed targets
            for t_id in list(workers.keys()):
                if t_id not in current_target_ids:
                    workers[t_id].cancel()
                    del workers[t_id]

            await asyncio.sleep(poll_interval)
        except asyncio.CancelledError:
            for w in workers.values():
                w.cancel()
            break
        except Exception as e:
            logger.error(f"Daemon loop error: {e}")
            await asyncio.sleep(poll_interval)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ChatGPT CDP Injector")
    parser.add_argument("--once", action="store_true", help="Inject once and exit")
    parser.add_argument("--force", action="store_true", help="Force inject even if pill exists")
    parser.add_argument("--ports", nargs="+", type=int, default=[9223, 9224], help="DevTools ports to probe")
    args = parser.parse_args()

    if args.once:
        count = asyncio.run(scan_and_inject_once(ports=args.ports, force=args.force))
        print(f"Injected into {count} targets.")
    else:
        try:
            asyncio.run(daemon_loop(ports=args.ports))
        except KeyboardInterrupt:
            print("Stopped.")
