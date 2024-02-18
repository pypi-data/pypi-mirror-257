import os


def sub_names(path) -> tuple[list, list | None]:
    from .sub_paths import sub_paths
    ps, e = sub_paths(path)
    r = []
    for sp in ps:
        r.append(os.path.basename(sp))
    return r, e
