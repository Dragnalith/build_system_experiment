import pathlib
import utility

root = utility.find_root_mark('RootMark')
ninja = root / 'bin/win/ninja.exe'
gn = root / 'bin/win/gn.exe'
vswhere = root / 'bin/win/vswhere.exe'
variant_folder = root / 'project/build/variant'
build_root = root / 'project/_generated'
build_environment = build_root / 'environment'
verbose = False