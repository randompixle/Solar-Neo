from .base import Backend, OpResult
from ..utils.run import run, which

class DnfBackend(Backend):
    name = "dnf"
    priority = 50
    def _exe(self) -> str:
        return "dnf5" if which("dnf5") else "dnf"
    def available(self) -> bool:
        return which("dnf") is not None or which("dnf5") is not None
    def install(self, pkg: str) -> OpResult:
        return OpResult(run([self._exe(),"install","-y",pkg], use_sudo=True)==0)
    def remove(self, pkg: str) -> OpResult:
        return OpResult(run([self._exe(),"remove","-y",pkg], use_sudo=True)==0)
    def search(self, term: str) -> OpResult:
        return OpResult(run([self._exe(),"search",term])==0)
    def update(self) -> OpResult:
        return OpResult(run([self._exe(),"makecache"], use_sudo=True)==0)
    def upgrade(self) -> OpResult:
        return OpResult(run([self._exe(),"upgrade","-y"], use_sudo=True)==0)
    def info(self, pkg: str) -> OpResult:
        return OpResult(run([self._exe(),"info",pkg])==0)
    def list_installed(self) -> OpResult:
        return OpResult(run([self._exe(),"list","installed"])==0)
