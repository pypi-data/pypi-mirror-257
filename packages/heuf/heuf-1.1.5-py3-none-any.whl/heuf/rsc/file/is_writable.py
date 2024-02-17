import os


def is_writable(path) -> bool:
    from .is_exists import is_exists
    from .is_creatable import is_creatable
    if not is_exists(path):
        return is_creatable(path)
    if os.access(path, os.W_OK):
        return True
    return False
