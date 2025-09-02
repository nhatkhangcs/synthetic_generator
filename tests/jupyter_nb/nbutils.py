from types import ModuleType
import importlib
import pkgutil
import sys


def reload_package(package: ModuleType):
    """
    Reloads the specified package and all its submodules.

    Args:
        package: A reference to the imported package (not the package name as a string).
    """
    importlib.reload(package)
    for _, modname, _ in pkgutil.walk_packages(
        package.__path__, package.__name__ + "."
    ):
        if modname in sys.modules:
            importlib.reload(sys.modules[modname])
