def is_creatable(path) -> bool:
    from .is_exists import is_exists
    from ..dir.is_creatable import is_creatable as is_dir_creatable
    from ..dir.sir_dir_path import sir_dir_path as sir_dir_path
    if is_exists(path):
        return False
    return is_dir_creatable(sir_dir_path(path))
