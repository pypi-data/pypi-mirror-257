import shutil


def copy(src_path, dest_path) -> bool:
    from .is_creatable import is_creatable
    from .is_exists import is_exists
    from .is_readable import is_readable
    if not is_exists(src_path) or not is_readable(src_path):
        return False
    if is_exists(dest_path) or not is_creatable(dest_path):
        return False
    try:
        shutil.copytree(src_path, dest_path)
        return True
    except shutil.Error:
        return False
