import re
from .base import Backend, OpResult
from ..utils.run import run, run_capture, which

class FlatpakBackend(Backend):
    name = "flatpak"
    priority = 90
    def available(self) -> bool:
        return which("flatpak") is not None
    def _guess_appid(self, name: str):
        rc,out = run_capture(["flatpak","search",name])
        if rc!=0 or not out.strip(): return None
        for line in out.splitlines():
            parts = re.split(r"\s{2,}|\t", line.strip())
            if parts:
                cand = parts[0].strip()
                if "." in cand: return cand
        return None
    def install(self, pkg: str) -> OpResult:
        target = pkg if "." in pkg else (self._guess_appid(pkg) or pkg)
        return OpResult(run(["flatpak","install","-y","flathub",target])==0)
    def remove(self, pkg: str) -> OpResult:
        target = pkg if "." in pkg else (self._guess_appid(pkg) or pkg)
        return OpResult(run(["flatpak","uninstall","-y",target])==0)
    def search(self, term: str) -> OpResult:
        return OpResult(run(["flatpak","search",term])==0)
    def update(self) -> OpResult:
        run(["flatpak","update","--appstream"])
        return OpResult(True,0)
    def upgrade(self) -> OpResult:
        return OpResult(run(["flatpak","update","-y"])==0)
    def info(self, pkg: str) -> OpResult:
        target = pkg if "." in pkg else (self._guess_appid(pkg) or pkg)
        return OpResult(run(["flatpak","info",target])==0)
    def list_installed(self) -> OpResult:
        return OpResult(run(["flatpak","list"])==0)
