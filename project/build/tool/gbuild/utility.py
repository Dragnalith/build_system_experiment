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

def generate_environment_block(env):
    block = ''
    nul = '\0'
    for key, value in env.items():
        block += key + '=' + value + nul
    block += nul

    return block

def write_environment_block(filepath, env):
    """
        Write a dict as a file using the format required by the windows API CreateProcess to
        specify environment variable for the process. The file can be read as a raw buffer and
        a pointer to that buffer can be given to CreateProcess without any required processing.
    """
    filepath.parent.mkdir(parents=True,exist_ok=True)

    with open(filepath, 'w') as f:
        f.write(generate_environment_block(env))

def write_ninja_file(filepath, env):
    """
        Write variable with the ninja file format.
        So the output file can be included by another ninja file.
    """
    filepath.parent.mkdir(parents=True,exist_ok=True)

    with open(filepath, 'w') as f:
        for key, value in env.items():
            f.write("{}={}\n".format(key,value))

class IncompatibleTypeError(Exception):
    """Requested folder has not been found"""
    pass

def convert_to_gn_str(value):
    if isinstance(value, str):
        return '"{}"'.format(value.replace('"','\\"'))

    if isinstance(value, int):
        return str(value)

    if isinstance(value, pathlib.Path):
        value.resolve()
        return convert_to_gn_str(str(value))

    raise IncompatibleTypeError('The type {} cannot be converted to gn value'.format(type(value)))

def clean_dir(path):
    """
        Remove a directory recursively. Does not stop if removing a file fail, remove the maximum
    """

    path = pathlib.Path(path)
    all_removed = True
    for child in path.glob('*'):
        if child.is_file():
            try:
                child.unlink()
            except:
                all_removed = False
                print("WARNING: {} could not be removed".format(child))
        else:
            all_removed = clean_dir(child) and all_removed
    
    if all_removed:
        try:
            path.rmdir()
        except:
            print("WARNING: {} could not be removed".format(child))
            
        return True
    
    return False