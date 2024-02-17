import os
from .sub_paths import sub_paths


def sub_dir_paths(path) -> list:
    paths = sub_paths(path)
    result = []
    for sub_path in paths:
        if os.path.isdir(sub_path):
            result.append(sub_path)
    return result
