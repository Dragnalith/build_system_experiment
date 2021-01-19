import pathlib
import utility

# Global Values    
vs_version = '2019'
verbose = False

root = utility.find_root_mark('RootMark')
ninja = root / 'bin/win/ninja.exe'
gn = root / 'bin/win/gn.exe'
vswhere = root / 'bin/win/vswhere.exe'
variant_folder = root / 'project/build/variant'
build_root = root / 'project/_generated'
build_root.mkdir(parents=True, exist_ok=True)
build_environment = build_root / 'environment'
variant_path_filename = 'variant.txt'

# List available variants
builtin_variants = set([x.name for x in variant_folder.iterdir()])
variants = builtin_variants.copy()

if build_root.is_dir():
    for d in build_root.iterdir():
        p = d / variant_path_filename
        if p.exists():
            variants.add(d.name)

# Find last variants

last_variant = build_root / 'last_variant.txt'

default_variant = 'debug'
if not default_variant in variants:
    default_variant = next(iter(variants))

if last_variant.exists():
    last = last_variant.read_text()
    if last in variants:
        default_variant = last
    else:
        last_variant.unlink()
