import os


def is_creatable(path) -> tuple[bool, list | None]:
    from .is_exists import is_exists
    from .is_writable import is_writable
    r, e = is_exists(path)
    if r:
        return False, e
    # 基本情况：如果已经递归到根目录，终止递归
    rp = os.path.dirname(path)
    if path == rp or path == rp + os.path.sep:
        return False, ['{path} root path is not creatable']
    if is_exists(rp)[0]:
        return is_writable(rp)
    return is_creatable(rp)
