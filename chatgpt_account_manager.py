#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatGPT Desktop & OpenAI Codex Account & Profile Manager
Author: Antigravity Suite Team
Platform: Windows / macOS / Linux

Features:
- Multi-Account profile storage and instant switching for Codex (auth.json)
- Dual-Instance concurrent execution (Instance 1 & Instance 2 with isolated user-data-dir)
- Remote debugging launcher for UI theming and CDP injection
- Safe backup and restoration of session states
"""

import os
import sys
import json
import glob
import shutil
import base64
import time
import socket
import subprocess
from pathlib import Path

# Base Paths
USER_HOME = Path.home()
CODEX_HOME = Path(os.getenv("CODEX_HOME", str(USER_HOME / ".codex")))
AUTH_JSON_PATH = CODEX_HOME / "auth.json"
PROFILES_DIR = CODEX_HOME / "profiles"
CHATGPT_SETTINGS_FILE = CODEX_HOME / "chatgpt_suite_settings.json"

LOCAL_APP_DATA = Path(os.getenv("LOCALAPPDATA", str(USER_HOME / "AppData" / "Local")))
INSTANCE2_USER_DATA = LOCAL_APP_DATA / "OpenAI" / "ChatGPT-Instance2"

DEFAULT_SETTINGS = {
    "active_profile": "default",
    "theme": "clean_dark",
    "colorMode": "accent",
    "strokeMode": "none",
    "fontFa": "Vazirmatn",
    "fontEn": "default",
    "rtl": True,
    "devtools_port_1": 9223,
    "devtools_port_2": 9224,
    "auto_inject": True
}

def get_chatgpt_exe_path():
    """Detects the installed ChatGPT.exe on Windows or macOS dynamically."""
    if sys.platform == "win32":
        # 1. Query Get-AppxPackage directly (fast, authoritative, handles any Store update)
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "(Get-AppxPackage *OpenAI*).InstallLocation"],
                capture_output=True,
                text=True,
                timeout=5
            )
            loc = res.stdout.strip()
            if loc:
                cand = Path(loc) / "app" / "ChatGPT.exe"
                if cand.exists():
                    return str(cand)
        except Exception:
            pass

        # 2. Check wildcard matches in WindowsApps
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "(Get-Item 'C:\\Program Files\\WindowsApps\\OpenAI.Codex_*\\app\\ChatGPT.exe' -ErrorAction SilentlyContinue | Select-Object -Last 1).FullName"],
                capture_output=True,
                text=True,
                timeout=4
            )
            loc = res.stdout.strip()
            if loc and Path(loc).exists():
                return loc
        except Exception:
            pass

        # 3. Fallback to local appdata
        local_cand = LOCAL_APP_DATA / "OpenAI" / "Codex" / "ChatGPT.exe"
        if local_cand.exists():
            return str(local_cand)
    elif sys.platform == "darwin":
        cands = [
            Path("/Applications/ChatGPT.app/Contents/MacOS/ChatGPT"),
            USER_HOME / "Applications" / "ChatGPT.app" / "Contents" / "MacOS" / "ChatGPT"
        ]
        for c in cands:
            if c.exists():
                return str(c)
    return None

def get_codex_cli_path():
    """Finds the codex.exe CLI executable."""
    if sys.platform == "win32":
        bin_dir = LOCAL_APP_DATA / "OpenAI" / "Codex" / "bin"
        if bin_dir.exists():
            matches = list(bin_dir.glob("*/codex.exe"))
            if matches:
                matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return str(matches[0])
    return "codex"

def load_settings():
    if CHATGPT_SETTINGS_FILE.exists():
        try:
            with open(CHATGPT_SETTINGS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                res = dict(DEFAULT_SETTINGS)
                res.update(saved)
                return res
        except Exception:
            pass
    return dict(DEFAULT_SETTINGS)

def save_settings(patch):
    cur = load_settings()
    cur.update(patch)
    try:
        CHATGPT_SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CHATGPT_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(cur, f, indent=2, ensure_ascii=False)
        return True, cur
    except Exception as e:
        return False, str(e)

def extract_email_from_token(token_str):
    """Parses a JWT payload to extract user email or sub without external dependencies."""
    if not token_str or not isinstance(token_str, str):
        return None
    try:
        parts = token_str.split(".")
        if len(parts) >= 2:
            payload_b64 = parts[1]
            # Add padding if needed
            rem = len(payload_b64) % 4
            if rem > 0:
                payload_b64 += "=" * (4 - rem)
            decoded = base64.urlsafe_b64decode(payload_b64).decode("utf-8", errors="ignore")
            data = json.loads(decoded)
            return (
                data.get("email") or 
                data.get("https://api.openai.com/profile", {}).get("email") or 
                data.get("preferred_username") or
                data.get("name") or
                data.get("sub")
            )
    except Exception:
        pass
    return None

def read_active_auth_metadata():
    """Reads ~/.codex/auth.json and returns non-sensitive metadata."""
    if not AUTH_JSON_PATH.exists():
        return {"exists": False}
    try:
        with open(AUTH_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        auth_mode = data.get("auth_mode", "unknown")
        last_refresh = data.get("last_refresh")
        
        email = None
        tokens = data.get("tokens", {})
        if isinstance(tokens, dict):
            # Check id_token or access_token
            for key in ["id_token", "access_token"]:
                tok = tokens.get(key)
                if tok:
                    found_email = extract_email_from_token(tok)
                    if found_email:
                        email = found_email
                        break
            # Check account_id
            account_id = tokens.get("account_id")
        else:
            account_id = None

        return {
            "exists": True,
            "auth_mode": auth_mode,
            "last_refresh": last_refresh,
            "email": email or "Active User",
            "account_id": account_id
        }
    except Exception as e:
        return {"exists": True, "error": str(e), "email": "Active User"}

def list_profiles():
    """Returns all registered profiles with their metadata."""
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    profiles = []
    
    settings = load_settings()
    active_profile_id = settings.get("active_profile", "default")
    active_meta = read_active_auth_metadata()

    # Check existing profile folders
    for entry in PROFILES_DIR.iterdir():
        if entry.is_dir():
            meta_file = entry / "profile.json"
            meta = {}
            if meta_file.exists():
                try:
                    with open(meta_file, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                except Exception:
                    meta = {}
            
            p_id = entry.name
            display_name = meta.get("display_name", p_id)
            email = meta.get("email", "Unknown")
            is_active = (p_id == active_profile_id)
            
            profiles.append({
                "id": p_id,
                "display_name": display_name,
                "email": email,
                "created_at": meta.get("created_at"),
                "is_active": is_active,
                "has_auth": (entry / "auth.json").exists()
            })

    # If no profile exists yet, seed 'default' from active auth if available
    if not profiles and active_meta.get("exists"):
        default_dir = PROFILES_DIR / "default"
        default_dir.mkdir(exist_ok=True)
        try:
            shutil.copy2(AUTH_JSON_PATH, default_dir / "auth.json")
            meta = {
                "id": "default",
                "display_name": "Account 1 (Main)",
                "email": active_meta.get("email", "Main Account"),
                "created_at": time.time()
            }
            with open(default_dir / "profile.json", "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
            profiles.append({
                "id": "default",
                "display_name": meta["display_name"],
                "email": meta["email"],
                "created_at": meta["created_at"],
                "is_active": True,
                "has_auth": True
            })
        except Exception:
            pass

    return {
        "active_profile": active_profile_id,
        "active_meta": active_meta,
        "profiles": profiles
    }

def save_current_profile(profile_id, display_name=None, email=None):
    """Saves the current auth.json as a saved profile."""
    if not AUTH_JSON_PATH.exists():
        return False, "No active auth.json found to save."
    
    clean_id = "".join(c for c in profile_id if c.isalnum() or c in ("-", "_")).lower()
    if not clean_id:
        return False, "Invalid profile ID."

    target_dir = PROFILES_DIR / clean_id
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(AUTH_JSON_PATH, target_dir / "auth.json")
        active_meta = read_active_auth_metadata()
        resolved_email = email or active_meta.get("email") or "Unknown"
        resolved_name = display_name or clean_id.capitalize()

        meta = {
            "id": clean_id,
            "display_name": resolved_name,
            "email": resolved_email,
            "saved_at": time.time()
        }
        with open(target_dir / "profile.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        save_settings({"active_profile": clean_id})
        return True, meta
    except Exception as e:
        return False, str(e)

def switch_profile(profile_id):
    """Switches ~/.codex/auth.json to the target profile and restarts Codex daemon."""
    clean_id = "".join(c for c in profile_id if c.isalnum() or c in ("-", "_")).lower()
    target_dir = PROFILES_DIR / clean_id
    target_auth = target_dir / "auth.json"

    if not target_auth.exists():
        return False, f"Profile '{clean_id}' does not have an auth.json file."

    try:
        # 1. Backup current active auth.json
        if AUTH_JSON_PATH.exists():
            backup_path = CODEX_HOME / "auth.json.bak"
            shutil.copy2(AUTH_JSON_PATH, backup_path)

        # 2. Swap auth.json
        shutil.copy2(target_auth, AUTH_JSON_PATH)

        # 3. Update settings
        save_settings({"active_profile": clean_id})

        # 4. Restart or signal codex background processes
        restart_codex_app_server()

        return True, f"Successfully switched to profile '{clean_id}'."
    except Exception as e:
        return False, str(e)

def restart_codex_app_server():
    """Kills existing codex background daemon so it reloads the new auth.json."""
    if sys.platform == "win32":
        try:
            # Kill codex app-server processes gracefully
            subprocess.run(
                ["powershell", "-Command", "Get-Process codex -ErrorAction SilentlyContinue | Where-Object { $_.Path -match 'Codex' } | Stop-Process -Force -ErrorAction SilentlyContinue"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )
        except Exception:
            pass

def trigger_codex_login(mode='oauth', api_key=None):
    """
    Triggers Codex / ChatGPT login flow:
    - 'oauth': launches `codex login` which opens default browser for official OpenAI OAuth.
    - 'api_key': authenticates using OpenAI API Key via `codex login --with-api-key`.
    - 'web': opens official ChatGPT web sign-in page.
    """
    codex_cli = get_codex_cli_path()
    if mode == 'api_key' and api_key:
        try:
            res = subprocess.run(
                [codex_cli, "login", "--with-api-key"],
                input=api_key.strip(),
                capture_output=True,
                text=True,
                timeout=15
            )
            restart_codex_app_server()
            return (res.returncode == 0), res.stdout.strip() or res.stderr.strip() or "API Key authenticated."
        except Exception as e:
            return False, str(e)
    elif mode == 'web':
        import webbrowser
        webbrowser.open("https://chatgpt.com/auth/login")
        return True, "Opened ChatGPT login page in browser."
    else:  # oauth (default)
        try:
            DETACHED_PROCESS = 0x00000008 if sys.platform == 'win32' else 0
            CREATE_NEW_PROCESS_GROUP = 0x00000200 if sys.platform == 'win32' else 0
            subprocess.Popen([codex_cli, "login"], creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
            return True, "OAuth login launched. Complete sign-in in your default browser."
        except Exception as e:
            return False, str(e)

def trigger_codex_logout():
    """Removes stored authentication credentials and resets active session."""
    codex_cli = get_codex_cli_path()
    try:
        subprocess.run([codex_cli, "logout"], capture_output=True, timeout=10)
    except Exception:
        pass

    if AUTH_JSON_PATH.exists():
        try:
            backup_path = CODEX_HOME / "auth.json.bak"
            shutil.copy2(AUTH_JSON_PATH, backup_path)
            AUTH_JSON_PATH.unlink()
        except Exception:
            pass

    restart_codex_app_server()
    return True, "Logged out successfully. You can now log into another account."

def is_port_open(port):
    """Checks if a TCP port is open locally across candidate interfaces."""
    hosts = ["127.0.0.1", "localhost"]
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if ip not in hosts:
                hosts.append(ip)
    except Exception:
        pass
    for host in hosts:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                if s.connect_ex((host, int(port))) == 0:
                    return True
        except Exception:
            pass
    return False

def launch_chatgpt(instance_num=1, new_window=False, workspace_path=None):
    """
    Launches ChatGPT Desktop safely with remote debugging instrumentation:
    - instance_num 1: Standard profile launched via official Store AppContainer with DevTools port
    - instance_num 2: Isolated user-data-dir
    """
    settings = load_settings()
    port = settings.get("devtools_port_1", 9223) if instance_num == 1 else settings.get("devtools_port_2", 9224)

    if sys.platform == "win32" and instance_num == 1 and not new_window:
        # If port is not listening yet, close any uninstrumented background instance first
        if not is_port_open(port):
            try:
                subprocess.run(
                    ["powershell", "-NoProfile", "-Command", "Stop-Process -Name ChatGPT -Force -ErrorAction SilentlyContinue"],
                    timeout=5
                )
                time.sleep(1.2)
            except Exception:
                pass
        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", f"Start-Process -FilePath 'shell:AppsFolder\\OpenAI.Codex_2p2nqsd0c76g0!App' -ArgumentList '--remote-debugging-port={port}'"],
                timeout=5
            )
            return True, f"Launched ChatGPT Instance 1 via Windows Application Manager with DevTools port {port}"
        except Exception:
            pass

    exe = get_chatgpt_exe_path()
    if not exe:
        codex_cli = get_codex_cli_path()
        cmd = [codex_cli, "app"]
        if workspace_path:
            cmd.append(str(workspace_path))
        subprocess.Popen(cmd)
        return True, "Launched via Codex CLI"

    settings = load_settings()
    port = settings.get("devtools_port_1", 9223) if instance_num == 1 else settings.get("devtools_port_2", 9224)

    cmd = [exe]
    if instance_num == 2:
        INSTANCE2_USER_DATA.mkdir(parents=True, exist_ok=True)
        cmd.append(f'--user-data-dir={INSTANCE2_USER_DATA}')

    if new_window:
        cmd.append("--new-window")

    if workspace_path:
        cmd.append(str(workspace_path))

    try:
        root_dir = str(Path(exe).parent.parent) if "WindowsApps" in exe else str(Path(exe).parent)
        if sys.platform == "win32":
            subprocess.Popen(cmd, cwd=root_dir)
        else:
            subprocess.Popen(cmd, cwd=root_dir, start_new_session=True)
        return True, f"Launched ChatGPT Instance {instance_num}"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ChatGPT & Codex Account Manager")
    parser.add_argument("--list", action="store_true", help="List all saved profiles")
    parser.add_argument("--save", metavar="PROFILE_ID", help="Save active session as profile")
    parser.add_argument("--name", help="Display name for saved profile")
    parser.add_argument("--switch", metavar="PROFILE_ID", help="Switch active profile")
    parser.add_argument("--launch", type=int, choices=[1, 2], help="Launch instance 1 or 2")
    parser.add_argument("--new-window", action="store_true", help="Open new window")

    args = parser.parse_args()

    if args.list:
        data = list_profiles()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.save:
        ok, res = save_current_profile(args.save, display_name=args.name)
        print(f"Result: {ok} -> {res}")
    elif args.switch:
        ok, res = switch_profile(args.switch)
        print(f"Result: {ok} -> {res}")
    elif args.launch:
        ok, res = launch_chatgpt(instance_num=args.launch, new_window=args.new_window)
        print(f"Result: {ok} -> {res}")
    else:
        parser.print_help()
