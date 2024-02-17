def append(path, content) -> bool:
    from .is_writable import is_writable
    if not is_writable(path):
        return False
    with open(path, 'a') as file:
        # 写入内容到文件
        file.write(content)
    return True
