import pathlib
import settings
import utility

import sdk.winsdk as winsdk

class EnvironmentFile:
    def __init__(self, name, generator):
        self.name = name
        self.path = settings.build_environment / name
        self.generator = generator

files = dict()

def _add(name, generator):
    files[name] = EnvironmentFile(name, generator)

def generate_winsdk():
    winsdk_config = winsdk.get_latest_config()

    content = ""
    content += 'include = {}\n'.format(utility.convert_to_gn_str(winsdk_config.include_path))
    content += 'lib = {}\n'.format(utility.convert_to_gn_str(winsdk_config.lib_path))
    content += 'root = {}\n'.format(utility.convert_to_gn_str(winsdk_config.install_path))

    return content;

_add('winsdk', generate_winsdk)

def generate():
    pathlib.Path(settings.build_environment).mkdir(parents=True, exist_ok=True)
    for name, f in files.items():
        with open(f.path, "w") as file:
            file.write(f.generator())
        print('    generate: {}'.format(f.path))

def all_exists():
    for name, f in files.items():
        if not f.path.exists():
            return False
            
    return True