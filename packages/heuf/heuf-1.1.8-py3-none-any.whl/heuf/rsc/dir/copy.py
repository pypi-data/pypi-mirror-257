import shutil


def copy(src_path, dest_path) -> tuple[bool, list | None]:
    from .is_creatable import is_creatable
    from .is_exists import is_exists
    from .is_readable import is_readable
    r, e = is_readable(src_path)
    if not r:
        return False, e
    r, e = is_exists(dest_path)
    if not r:
        return False, e
    r, e = is_creatable(dest_path)
    if not r:
        return False, e
    try:
        shutil.copytree(src_path, dest_path)
        return True, None
    except shutil.Error as e:
        return False, [e]
