import os


def sub_paths(path) -> tuple[list, list | None]:
    from .is_exists import is_exists
    r, e = is_exists(path)
    if not r:
        return [], e
    return os.listdir(path), None
