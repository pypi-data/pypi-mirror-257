import os
from .is_exists import is_exists


def sub_paths(path) -> list:
    if not is_exists(path):
        return []
    return os.listdir(path)
