import os.path


def sub_path(path: str, name: str) -> tuple[str, list | None]:
    return os.path.join(path, name), None
