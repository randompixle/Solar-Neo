import importlib, pkgutil, os, tomllib
from typing import List, Type
from .backends.base import Backend
from .utils.pretty import info

def load_config():
    # Minimal config loader
    home = os.path.expanduser("~")
    path = os.path.join(home, ".config", "neo", "config.toml")
    cfg = {"color": True, "aur_auto_offer": True}
    try:
        with open(path, "rb") as f:
            cfg.update(tomllib.load(f))
    except FileNotFoundError:
        pass
    return cfg

def load_backends() -> List[Backend]:
    import neo.backends
    backends: List[Backend] = []
    for _, modname, _ in pkgutil.iter_modules(neo.backends.__path__):
        module = importlib.import_module(f"neo.backends.{modname}")
        for attr in dir(module):
            cls = getattr(module, attr)
            if isinstance(cls, type) and issubclass(cls, Backend) and cls is not Backend:
                backends.append(cls())
    backends.sort(key=lambda b: b.priority)
    return backends
