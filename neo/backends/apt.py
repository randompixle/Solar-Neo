from .base import Backend, OpResult
from ..utils.run import run, which

class AptBackend(Backend):
    name = "apt"
    priority = 40
    def available(self) -> bool:
        return which("apt") is not None
    def install(self, pkg: str) -> OpResult:
        return OpResult(run(["apt","install","-y",pkg], use_sudo=True)==0)
    def remove(self, pkg: str) -> OpResult:
        return OpResult(run(["apt","remove","-y",pkg], use_sudo=True)==0)
    def search(self, term: str) -> OpResult:
        return OpResult(run(["apt","search",term])==0)
    def update(self) -> OpResult:
        return OpResult(run(["apt","update"], use_sudo=True)==0)
    def upgrade(self) -> OpResult:
        return OpResult(run(["apt","upgrade","-y"], use_sudo=True)==0)
    def info(self, pkg: str) -> OpResult:
        return OpResult(run(["apt","show",pkg])==0)
    def list_installed(self) -> OpResult:
        return OpResult(run(["apt","list","--installed"])==0)
