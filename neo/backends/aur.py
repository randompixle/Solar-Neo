from .base import Backend, OpResult
from ..utils.run import run, which

class AurBackend(Backend):
    name = "aur"
    priority = 35
    helper = None
    def available(self) -> bool:
        self.helper = which("yay") or which("paru")
        return self.helper is not None
    def install(self, pkg: str) -> OpResult:
        return OpResult(run([self.helper,"-S","--noconfirm",pkg], use_sudo=False)==0)
    def remove(self, pkg: str) -> OpResult:
        return OpResult(run([self.helper,"-R","--noconfirm",pkg], use_sudo=False)==0)
    def search(self, term: str) -> OpResult:
        return OpResult(run([self.helper,"-Ss",term])==0)
    def update(self) -> OpResult:
        return OpResult(True,0)
    def upgrade(self) -> OpResult:
        return OpResult(run([self.helper,"-Su","--noconfirm"], use_sudo=False)==0)
    def info(self, pkg: str) -> OpResult:
        return OpResult(run([self.helper,"-Si",pkg])==0)
    def list_installed(self) -> OpResult:
        return OpResult(run([self.helper,"-Q"])==0)
