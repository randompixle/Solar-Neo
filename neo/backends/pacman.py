from .base import Backend, OpResult
from ..utils.run import run, which

class PacmanBackend(Backend):
    name = "pacman"
    priority = 30
    def available(self) -> bool:
        return which("pacman") is not None
    def install(self, pkg: str) -> OpResult:
        run(["pacman","-Sy"], use_sudo=True)
        return OpResult(run(["pacman","-S","--noconfirm",pkg], use_sudo=True)==0)
    def remove(self, pkg: str) -> OpResult:
        return OpResult(run(["pacman","-R","--noconfirm",pkg], use_sudo=True)==0)
    def search(self, term: str) -> OpResult:
        return OpResult(run(["pacman","-Ss",term])==0)
    def update(self) -> OpResult:
        return OpResult(run(["pacman","-Sy"], use_sudo=True)==0)
    def upgrade(self) -> OpResult:
        return OpResult(run(["pacman","-Su","--noconfirm"], use_sudo=True)==0)
    def info(self, pkg: str) -> OpResult:
        return OpResult(run(["pacman","-Si",pkg])==0)
    def list_installed(self) -> OpResult:
        return OpResult(run(["pacman","-Q"])==0)
