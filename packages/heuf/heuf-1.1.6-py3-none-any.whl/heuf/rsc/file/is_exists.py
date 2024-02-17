import os


def is_exists(path) -> bool:
    if not os.path.exists(path):
        return False
    if os.path.isfile(path):
        return True
    return False
