import os


def is_readable(path) -> bool:
    from .is_exists import is_exists
    if not is_exists(path):
        return False
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
    if os.access(path, os.R_OK):
        return True
    return False
