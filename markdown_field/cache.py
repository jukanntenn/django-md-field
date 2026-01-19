import uuid
from typing import Any, Dict, Optional

_field_registry: Dict[str, Dict[str, Any]] = {}


def register_field(extensions: list, extension_configs: dict) -> str:
    """Register a Markdown field configuration and return a cache key."""
    key = str(uuid.uuid4())
    _field_registry[key] = {
        "extensions": extensions,
        "extension_configs": extension_configs,
    }
    return key


def get_field_config(key: str) -> Optional[Dict[str, Any]]:
    """Get field configuration by cache key."""
    return _field_registry.get(key)


def clear_cache() -> None:
    """Clear all cached field configurations. Useful for testing."""
    _field_registry.clear()
