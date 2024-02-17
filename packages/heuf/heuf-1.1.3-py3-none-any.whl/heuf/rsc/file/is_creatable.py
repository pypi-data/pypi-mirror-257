import os
from .is_exists import is_exists
from ..dir.is_creatable import is_creatable as is_dir_creatable


def is_creatable(path) -> bool:
    if is_exists(path):
        return False
    return is_dir_creatable(os.path.dirname(path))
