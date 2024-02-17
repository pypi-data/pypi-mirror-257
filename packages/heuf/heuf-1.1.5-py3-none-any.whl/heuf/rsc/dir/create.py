import os


def create(path) -> bool:
    from .is_creatable import is_creatable
    if not is_creatable(path):
        return False
    return os.makedirs(path) is None
