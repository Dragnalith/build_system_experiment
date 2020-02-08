import pathlib

class FolderNotFound(Exception):
    """Requested folder has not been found"""
    pass

def find_root_mark(mark: str):
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
    filepath.parent.mkdir(parents=True,exist_ok=True)
    with open(filepath, 'w') as f:
        block = ''
        nul = '\0'
        for key, value in env.items():
            block += key + '=' + value + nul
        block += nul
        f.write(block)

def write_ninja_file(filepath, env):
    filepath.parent.mkdir(parents=True,exist_ok=True)
    with open(filepath, 'w') as f:
        for key, value in env.items():
            f.write("{}={}\n".format(key,value))

