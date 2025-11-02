import os, sys, argparse
from . import __version__
from .loader import load_backends, load_config
from .utils.pretty import ok, err, warn, info, big, celebrate
from .utils.run import which, run, run_capture, require_network_tools

def detect_active():
    bks = load_backends()
    active = [b for b in bks if b.available()]
    return bks, active

def prompt_setup_if_needed():
    # Recommend setup if flatpak or flathub missing; prompt user
    needs = []
    if not which("flatpak"):
        needs.append("flatpak")
    else:
        rc, out = run_capture(["flatpak","remotes"])
        if rc==0 and "flathub" not in out:
            needs.append("flathub")

    if needs:
        warn("Full functionality not ready — setup recommended.")
        ans = input("Run `neo setup` now? [Y/n] ").strip().lower()
        if ans in ("", "y", "yes"):
            do_setup(needs)
        else:
            info("OK — you can run `neo setup` later.")

def do_setup(needs=None):
    big("Preparing system…")
    # Try to enable flatpak + flathub for all distros
    if not which("flatpak"):
        # Attempt install via common managers
        if which("dnf") or which("dnf5"):
            run([("dnf5" if which("dnf5") else "dnf"),"install","-y","flatpak"], use_sudo=True)
        elif which("apt"):
            run(["apt","update"], use_sudo=True)
            run(["apt","install","-y","flatpak"], use_sudo=True)
        elif which("pacman"):
            run(["pacman","-Sy"], use_sudo=True)
            run(["pacman","-S","--noconfirm","flatpak"], use_sudo=True)
        else:
            warn("No known system package manager detected for installing flatpak.")
    if which("flatpak"):
        rc,_ = run_capture(["flatpak","remotes"])
        if rc==0:
            run(["flatpak","remote-add","--if-not-exists","flathub","https://dl.flathub.org/repo/flathub.flatpakrepo"])
        ok("Flatpak/Flathub ready")
    ok("System prepared")

def list_backends():
    bks, active = detect_active()
    names_active = {b.name for b in active}
    print("Backends:")
    for b in bks:
        mark = "active" if b.name in names_active else "available" if b.available() else "inactive"
        symbol = "✔" if mark=="active" else ("…" if mark=="available" else "✖")
        print(f" {symbol} {b.name:12} {mark} (priority {b.priority})")

def unified_list():
    _, active = detect_active()
    print("Installed (by backend):")
    for b in active:
        print(f"--- {b.name} ---")
        res = b.list_installed()
        if not res.ok:
            warn(f"{b.name}: could not list installed items")

def try_op(op, arg=None):
    _, active = detect_active()
    # prefer non-flatpak first
    natives = [b for b in active if b.name!="flatpak"]
    flat = [b for b in active if b.name=="flatpak"]
    ordered = natives + flat

    for b in ordered:
        info(f"Trying {b.name}…")
        fn = getattr(b, op)
        res = fn(arg) if arg is not None else fn()
        if res.ok:
            ok(f"{op} via {b.name}")
            return 0
    err("no backend succeeded")
    return 1

def self_update():
    big("Updating neo…")
    tool = require_network_tools()
    if not tool:
        err("Need curl or wget installed to self-update.")
        return 1
    # Placeholder: this prints instructions. (Implement real URL later.)
    print("Visit your GitHub release URL and download the latest zip, then run ./install.sh")
    celebrate("neo self-update complete (placeholder)")
    return 0

def entrypoint():
    parser = argparse.ArgumentParser(prog="neo", description="Universal APT-style installer for any Linux distro")
    parser.add_argument("-v","--version", action="store_true", help="show version and exit")

    sub = parser.add_subparsers(dest="cmd")

    for c in ("install","remove","search","info"):
        p = sub.add_parser(c, help=f"{c} a package")
        p.add_argument("name", help="package name or app-id")

    sub.add_parser("update", help="update repository metadata")
    sub.add_parser("upgrade", help="upgrade installed packages")
    sub.add_parser("list", help="list installed packages across backends")
    sub.add_parser("backend", help="list available backends").add_argument("action", nargs="?", default="list")
    sub.add_parser("setup", help="prepare the system (Flatpak/Flathub etc.)")
    sub.add_parser("self-update", help="update neo to the latest release")

    if len(sys.argv)==1:
        parser.print_help()
        return 0
    args = parser.parse_args()
    if args.version:
        print(f"neo v{__version__}")
        return 0

    # gentle first-run prompt
    if args.cmd not in ("setup","self-update","backend"):
        prompt_setup_if_needed()

    if args.cmd in ("install","remove","search","info"):
        return try_op(args.cmd, args.name)
    if args.cmd in ("update","upgrade"):
        return try_op(args.cmd)
    if args.cmd=="list":
        unified_list()
        return 0
    if args.cmd=="backend":
        if args.action=="list":
            list_backends()
            return 0
    if args.cmd=="setup":
        do_setup()
        return 0
    if args.cmd=="self-update":
        return self_update()

    parser.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(entrypoint())
