import os, re, shutil, subprocess, sys, time
from typing import List, Optional, Tuple

def shlex_join(parts: List[str]) -> str:
    out = []
    for p in parts:
        if re.search(r'\s|["\'\\]', p):
            out.append("'" + p.replace("'", "'\"'\"'") + "'")
        else:
            out.append(p)
    return " ".join(out)

def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)

def run(cmd: List[str], use_sudo: bool = False, check: bool = False) -> int:
    real_cmd = (["sudo"] + cmd) if use_sudo and os.geteuid() != 0 else cmd
    print("$ " + shlex_join(real_cmd))
    try:
        return subprocess.call(real_cmd)
    except FileNotFoundError:
        print(f"neo: command not found: {cmd[0]}", file=sys.stderr)
        return 127

def run_capture(cmd: List[str]) -> Tuple[int, str]:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return 0, out
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output
    except FileNotFoundError:
        return 127, ""

def require_network_tools() -> Optional[str]:
    # prefer curl then wget
    if which("curl"):
        return "curl"
    if which("wget"):
        return "wget"
    return None
