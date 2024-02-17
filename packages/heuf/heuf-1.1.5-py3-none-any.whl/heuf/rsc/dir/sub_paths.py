import os


def sub_paths(path) -> list:
    from .is_exists import is_exists
    if not is_exists(path):
        return []
    return os.listdir(path)
