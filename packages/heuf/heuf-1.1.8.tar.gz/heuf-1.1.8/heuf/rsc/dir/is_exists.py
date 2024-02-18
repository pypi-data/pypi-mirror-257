import os


def is_exists(path) -> tuple[bool, list | None]:
    if not os.path.exists(path) or not os.path.isdir(path):
        return False, [f'{path} does not exists']
    return True, None
