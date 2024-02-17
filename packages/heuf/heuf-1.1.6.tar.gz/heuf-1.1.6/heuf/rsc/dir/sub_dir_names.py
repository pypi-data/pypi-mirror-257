import os


def sub_dir_names(path) -> list:
    from .sub_dir_paths import sub_dir_paths
    paths = sub_dir_paths(path)
    result = []
    for sub_path in paths:
        result.append(os.path.basename(sub_path))
    return result
