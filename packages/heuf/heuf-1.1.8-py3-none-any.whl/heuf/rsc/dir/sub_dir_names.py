import os


def sub_dir_names(path) -> tuple[list, list | None]:
    from .sub_dir_paths import sub_dir_paths
    ps, e = sub_dir_paths(path)
    r = []
    for sp in ps:
        r.append(os.path.basename(sp))
    return r, e
