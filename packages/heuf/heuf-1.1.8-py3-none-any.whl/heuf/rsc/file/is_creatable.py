def is_creatable(path) -> tuple[bool, list | None]:
    from .is_exists import is_exists
    from ..dir.is_writable import is_writable as is_writable
    from .sir_dir_path import sir_dir_path as sir_dir_path
    r, e = is_exists(path)
    if r:
        return False, e
    return is_writable(sir_dir_path(path)[0])
