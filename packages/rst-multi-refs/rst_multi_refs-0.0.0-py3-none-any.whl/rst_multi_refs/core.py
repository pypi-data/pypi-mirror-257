"""Core (overall) features."""
import importlib
from pathlib import Path


def configure():
    """Set up using roles into docutils."""
    registry_dir = Path(__file__).parent / "registry"
    for path in registry_dir.glob("*.py"):
        if path.stem == "__init__":
            continue
        registry_module = importlib.import_module(f"..registry.{path.stem}", __name__)
        getattr(registry_module, "setup")()
