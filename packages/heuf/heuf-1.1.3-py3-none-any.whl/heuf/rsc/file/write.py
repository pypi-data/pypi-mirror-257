from .is_writable import is_writable


def write(path, content) -> bool:
    if not is_writable(path):
        return False
    with open(path, 'w') as file:
        # 写入内容到文件
        file.write(content)
    return True
