import pathlib

class FolderNotFound(Exception):
    """Requested folder has not been found"""
    pass

def find_root_mark(mark: str):
    """
        It will find the first folder in the hierarchy of the working directory which
        contains the file of name 'mark'.It will raise an error if such a folder does
        not exist
    """
    start_dir = pathlib.Path(__file__).parent
    current_dir = start_dir

    while not (current_dir / mark).exists():
        next_dir = current_dir.parent

        if next_dir == current_dir:
            raise FolderNotFound('The following "{}" root mark has not been found starting from {}'.format(mark, start_dir))
        else:
            current_dir = next_dir

    return current_dir

def write_environment_block(filepath, env):
    """
        Write a dict as a file using the format required by the windows API CreateProcess to
        specify environment variable for the process. The file can be read as a raw buffer and
        a pointer to that buffer can be given to CreateProcess without any required processing.
    """
    filepath.parent.mkdir(parents=True,exist_ok=True)
    with open(filepath, 'w') as f:
        block = ''
        nul = '\0'
        for key, value in env.items():
            block += key + '=' + value + nul
        block += nul
        f.write(block)

def write_ninja_file(filepath, env):
    """
        Write variable with the ninja file format.
        So the output file can be included by another ninja file.
    """
    filepath.parent.mkdir(parents=True,exist_ok=True)
    with open(filepath, 'w') as f:
        for key, value in env.items():
            f.write("{}={}\n".format(key,value))

