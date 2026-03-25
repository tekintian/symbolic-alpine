from __future__ import absolute_import
import os

__all__ = []

# Read version from version.txt
_version_file = os.path.join(os.path.dirname(__file__), '..', 'version.txt')
if os.path.exists(_version_file):
    with open(_version_file, 'r') as f:
        __version__ = f.read().strip()
else:
    __version__ = 'unknown'


def _import_all():
    import pkgutil

    glob = globals()
    for _, modname, _ in pkgutil.iter_modules(__path__):
        if modname[:1] == "_":
            continue
        mod = __import__("symbolic.%s" % modname, glob, glob, ["__name__"])
        if not hasattr(mod, "__all__"):
            continue
        __all__.extend(mod.__all__)
        for name in mod.__all__:
            obj = getattr(mod, name)
            if hasattr(obj, "__module__"):
                obj.__module__ = "symbolic"
            glob[name] = obj


_import_all()
del _import_all
