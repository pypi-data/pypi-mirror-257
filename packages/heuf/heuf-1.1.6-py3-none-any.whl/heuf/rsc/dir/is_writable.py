import os


def is_writable(path) -> bool:
    from .is_creatable import is_creatable
    from .is_exists import is_exists
    if not is_exists(path):
        return is_creatable(path)
    '''
    try:
        # 尝试写入一个临时文件
        with open(os.path.join(path, '.write_test'), 'w'):
            pass
        return True
    except IOError:
        return False
    finally:
        # 删除临时文件
        try:
            os.remove(os.path.join(path, '.write_test'))
        except OSError:
            pass
    '''
    if os.access(path, os.W_OK):
        return True
    return False
