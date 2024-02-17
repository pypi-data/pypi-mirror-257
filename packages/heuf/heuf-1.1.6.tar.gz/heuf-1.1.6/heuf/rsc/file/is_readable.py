import os


def is_readable(path) -> bool:
    from .is_exists import is_exists
    if not is_exists(path):
        return False
    if os.access(path, os.R_OK):
        return True
    return False
