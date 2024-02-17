import os


def sub_names(path) -> list:
    from .sub_paths import sub_paths
    paths = sub_paths(path)
    result = []
    for sub_path in paths:
        result.append(os.path.basename(sub_path))
    return result
