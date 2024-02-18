import shutil


def copy(src_path, dest_path) -> tuple[bool, list | None]:
    from .is_writable import is_writable
    from .is_readable import is_readable
    from .sir_dir_path import sir_dir_path
    r, e = is_readable(src_path)
    if r:
        return False, e
    return is_writable(sir_dir_path(dest_path)[0])
