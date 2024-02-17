import os
from .is_exists import is_exists
from .is_writable import is_writable


def is_creatable(path) -> bool:
    if is_exists(path):
        return False
    sir_path = os.path.dirname(path)
    # 基本情况：如果已经递归到根目录，终止递归
    root_path = os.path.dirname(sir_path)
    if sir_path == root_path or sir_path == root_path + os.path.sep:
        return False
    if is_exists(sir_path):
        return is_writable(sir_path)
    return is_creatable(sir_path)
