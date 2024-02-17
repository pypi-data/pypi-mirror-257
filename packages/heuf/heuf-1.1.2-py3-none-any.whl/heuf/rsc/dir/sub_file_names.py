import os
from .sub_file_paths import sub_file_paths


def sub_file_names(path) -> list:
    paths = sub_file_paths(path)
    result = []
    for sub_path in paths:
        result.append(os.path.basename(sub_path))
    return result
