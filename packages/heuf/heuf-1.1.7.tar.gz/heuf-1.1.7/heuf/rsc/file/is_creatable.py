def is_creatable(path) -> bool:
    from .is_exists import is_exists
    from ..dir.is_writable import is_writable as is_writable
    from .sir_dir_path import sir_dir_path as sir_dir_path
    if is_exists(path):
        return False
    return is_writable(sir_dir_path(path))
