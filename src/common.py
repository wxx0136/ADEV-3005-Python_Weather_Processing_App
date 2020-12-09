def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def mkdir_p(my_path):
    """Creates a directory. equivalent to using mkdir -p on the command line"""
    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(my_path)
    except OSError as exc:  # Python >2.5
        if exc.errno == EEXIST and path.isdir(my_path):
            pass
        else:
            raise
