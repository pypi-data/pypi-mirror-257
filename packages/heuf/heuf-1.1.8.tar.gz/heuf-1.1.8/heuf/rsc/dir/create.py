import os


def create(path) -> tuple[bool, list | None]:
    from .is_creatable import is_creatable
    r, e = is_creatable(path)
    if not r:
        return False, e
    try:
        os.makedirs(path)
        return True, None
    except Exception as e:
        return False, [e]
