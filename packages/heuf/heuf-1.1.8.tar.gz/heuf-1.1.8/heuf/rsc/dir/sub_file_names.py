import os


def sub_file_names(path) -> tuple[list, list | None]:
    from .sub_file_paths import sub_file_paths
    ps, e = sub_file_paths(path)
    r = []
    for sp in ps:
        r.append(os.path.basename(sp))
    return r, e
