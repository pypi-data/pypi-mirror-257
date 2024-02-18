import os


def is_readable(path) -> tuple[bool, list | None]:
    from .is_exists import is_exists
    r, e = is_exists(path)
    if not r:
        return False, e
    if not os.access(path, os.R_OK):
        return False, [f'{path} permission denied']
    return True, None
