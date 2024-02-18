import os.path


def sir_dir_path(path: str) -> tuple[str, list | None]:
    return os.path.dirname(path), None
