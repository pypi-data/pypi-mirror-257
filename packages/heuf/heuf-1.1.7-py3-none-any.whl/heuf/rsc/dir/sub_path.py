import os.path


def sub_path(path: str, name: str) -> str:
    return os.path.join(path, name)
