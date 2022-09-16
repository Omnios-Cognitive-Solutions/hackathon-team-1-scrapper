import os
import shutil


def make_absolute_path(relpath: str):
    return os.path.abspath(relpath)


def complete_relative_path(relpath: str):
    abspath = os.path.abspath(relpath)
    workdir = os.getcwd()
    return abspath.split(workdir)[1]


def clear_directory(path: str):
    try:
        cmd1 = f"rm -r {path} > /dev/null 2>&1"
        os.system(cmd1)
    except:
        pass
    try:
        cmd2 = f"mkdir {path} > /dev/null 2>&1"
        os.system(cmd2)
    except:
        pass


def get_extension(filepath: str):
    return os.path.splitext(filepath)[1]


def remove_extension(filepath: str):
    return os.path.splitext(filepath)[0]


def create_file(filepath: str, content: str):
    with open(filepath, "w") as f:
        f.write(content)
    return filepath


def copy_file(src: str, dst: str):
    return shutil.copyfile(src, dst)


def delete_file(filepath: str):
    return os.remove(filepath)


def get_filename(filepath: str, clear_extension: bool = False):
    filename = os.path.basename(filepath)
    if clear_extension:
        filename = remove_extension(filename)
    return filename


def add_suffix_to_filename(filepath: str, suffix: str):
    filepath_no_ext = remove_extension(filepath)
    ext = get_extension(filepath)
    filepath = f"{filepath_no_ext}{suffix}{ext}"
    return filepath


def add_prefix_to_filename(filepath: str, prefix: str):
    folderpath = os.path.dirname(filepath)
    filename = get_filename(filepath)
    ext = get_extension(filepath)
    filepath = f"{folderpath}/{prefix}{filename}{ext}"
    return filepath


def replace_extension(filepath: str, ext: str):
    filepath_no_ext = remove_extension(filepath)
    return f"{filepath_no_ext}.{ext}"
