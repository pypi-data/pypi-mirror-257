import os


def is_writable(path) -> tuple[bool, list | None]:
    from .is_creatable import is_creatable
    from .is_exists import is_exists
    if not is_exists(path):
        return is_creatable(path)
    if not os.access(path, os.W_OK):
        return False, [f'{path} permission denied']
    return True, None
