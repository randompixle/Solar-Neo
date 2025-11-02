import os, sys

# Minimal color handling; can be toggled off by config or NO_COLOR
USE_COLOR = os.environ.get("NO_COLOR") is None

def _c(code): 
    return f"\033[{code}m" if USE_COLOR and sys.stdout.isatty() else ""

BOLD = _c("1")
DIM = _c("2")
GREEN = _c("32")
RED = _c("31")
YELLOW = _c("33")
CYAN = _c("36")
RESET = _c("0")

def ok(msg): print(f"{GREEN}✔{RESET} {msg}")
def err(msg): print(f"{RED}✖{RESET} {msg}")
def warn(msg): print(f"{YELLOW}⚠{RESET} {msg}")
def info(msg): print(f"{CYAN}{msg}{RESET}")
def big(msg): print(f"🚀 {BOLD}{msg}{RESET}")
def celebrate(msg): print(f"🎉 {BOLD}{msg}{RESET}")
