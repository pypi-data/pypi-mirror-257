import os
from .is_creatable import is_creatable


def create(path) -> bool:
    if not is_creatable(path):
        return False
    return os.makedirs(path) is None
