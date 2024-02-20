import importlib.metadata as _metadata

from chemspyd import exceptions
from chemspyd.controller import Controller

__version__ = _metadata.version("chemspyd")

submodules = [
    "executor",
    "utils",
    "zones",
]

__all__ = [
    *submodules,
    "Controller",
    "exceptions",
    "__version__",
]


def __dir__():
    return __all__
