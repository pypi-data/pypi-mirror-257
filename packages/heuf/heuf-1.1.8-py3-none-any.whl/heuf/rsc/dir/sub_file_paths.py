import os


def sub_file_paths(path) -> tuple[list, list | None]:
    from .sub_paths import sub_paths
    ps, e = sub_paths(path)
    r = []
    for sp in ps:
        if os.path.isfile(sp):
            r.append(sp)
    return r, e
