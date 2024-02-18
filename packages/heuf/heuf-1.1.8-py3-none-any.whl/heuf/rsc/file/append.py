def append(path, content) -> tuple[bool, list | None]:
    from .is_writable import is_writable
    r, e = is_writable(path)
    if not r:
        return False, e
    with open(path, 'a') as file:
        # 写入内容到文件
        file.write(content)
    return True, None
