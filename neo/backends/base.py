from dataclasses import dataclass
from typing import Optional

@dataclass
class OpResult:
    ok: bool
    code: int = 0
    note: str = ""

class Backend:
    name = "base"
    priority = 100  # lower means earlier
    def available(self) -> bool: return False
    def install(self, pkg: str) -> OpResult: return OpResult(False, 1)
    def remove(self, pkg: str) -> OpResult: return OpResult(False, 1)
    def search(self, term: str) -> OpResult: return OpResult(False, 1)
    def update(self) -> OpResult: return OpResult(False, 1)
    def upgrade(self) -> OpResult: return OpResult(False, 1)
    def info(self, pkg: str) -> OpResult: return OpResult(False, 1)
    def list_installed(self) -> OpResult: return OpResult(False, 1)
