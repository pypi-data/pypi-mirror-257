from typing import Any


NULL_DICT: dict[Any, Any] = {}


def get_path(d: dict[str, Any], *args: str, default: Any = None) -> Any:
    for a in args:
        d = d.get(a, NULL_DICT)
        if d is NULL_DICT:
            return default

    return d
