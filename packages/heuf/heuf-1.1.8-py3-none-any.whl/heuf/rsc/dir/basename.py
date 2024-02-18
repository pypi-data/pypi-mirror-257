import os


def basename(path) -> tuple[str, list | None]:
    return os.path.basename(path), None
