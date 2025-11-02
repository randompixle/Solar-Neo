import os
from .base import Backend, OpResult
from ..utils.run import run, which

class RpmOstreeBackend(Backend):
    name = "rpm-ostree"
    priority = 20
    def available(self) -> bool:
        return os.path.exists("/run/ostree-booted") and which("rpm-ostree")
    def install(self, pkg: str) -> OpResult:
        ok = run(["rpm-ostree","install",pkg], use_sudo=True)==0
        if ok: print("⚠ Reboot (or apply-live) may be required.")
        return OpResult(ok)
    def remove(self, pkg: str) -> OpResult:
        ok = run(["rpm-ostree","uninstall",pkg], use_sudo=True)==0
        if ok: print("⚠ Reboot may be required.")
        return OpResult(ok)
    def search(self, term: str) -> OpResult:
        # proxy to dnf if present
        exe = "dnf5" if which("dnf5") else ("dnf" if which("dnf") else None)
        if exe:
            return OpResult(run([exe,"search",term])==0)
        print("Tip: Prefer Flatpak for apps on ostree.")
        return OpResult(False,1)
    def update(self) -> OpResult:
        return OpResult(run(["rpm-ostree","refresh-md"], use_sudo=True)==0)
    def upgrade(self) -> OpResult:
        ok = run(["rpm-ostree","upgrade"], use_sudo=True)==0
        if ok: print("⚠ Reboot to deploy the new image.")
        return OpResult(ok)
    def list_installed(self) -> OpResult:
        return OpResult(run(["rpm-ostree","status"])==0)
