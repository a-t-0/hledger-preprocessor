from typing import Dict


def dict_contains_string(d: Dict, substr: str, case_sensitive: bool) -> bool:
    if case_sensitive:
        return any(substr in str(value) for value in d.values())
    else:
        return any(substr.lower() in str(value).lower() for value in d.values())
