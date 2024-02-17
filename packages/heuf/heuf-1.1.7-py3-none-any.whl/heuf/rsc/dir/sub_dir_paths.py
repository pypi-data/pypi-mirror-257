import os


def sub_dir_paths(path) -> list:
    from .sub_paths import sub_paths
    paths = sub_paths(path)
    result = []
    for sub_path in paths:
        if os.path.isdir(sub_path):
            result.append(sub_path)
    return result
