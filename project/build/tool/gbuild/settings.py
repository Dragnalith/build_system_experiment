import pathlib

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

root = find_root_mark('RootMark')
ninja = root / 'bin/win/ninja.exe'
gn = root / 'bin/win/gn.exe'
vswhere = root / 'bin/win/vswhere.exe'
variant_folder = root / 'project/build/variant'
build_root = root / 'project/_generated'
verbose = False