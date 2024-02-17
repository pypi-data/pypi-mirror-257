import os


def is_exists(path) -> bool:
    if not os.path.exists(path):
        return False
    if os.path.isdir(path):
        return True
    return False
