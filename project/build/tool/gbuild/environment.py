import os
import pathlib
import settings
import utility

import sdk.winsdk as winsdk
import sdk.vstudio as vstudio

class EnvironmentFile:
    def __init__(self, name, generator):
        self.name = name
        self.path = settings.build_environment / name
        self.generator = generator

files = dict()

def _add(name, generator):
    files[name] = EnvironmentFile(name, generator)

_msvc_config = dict();

def _get_msvc_config(arch):
    if not arch in _msvc_config:
        _msvc_config[arch] = vstudio.get_msvc_config(settings.vs_version, arch)
        
    return _msvc_config[arch]
    

def generate_msvc(arch):  
    assert(arch in ['x86', 'x64'])

    msvc_config = _get_msvc_config(arch)

    content = ""
    content += 'include = {}\n'.format(utility.convert_to_gn_str(msvc_config.msvc_include))
    content += 'lib = {}\n'.format(utility.convert_to_gn_str(msvc_config.msvc_lib))
    content += 'bin = {}\n'.format(utility.convert_to_gn_str(msvc_config.msvc_bin))
    content += 'root = {}\n'.format(utility.convert_to_gn_str(msvc_config.msvc_path))
    content += 'msbuild = {}\n'.format(utility.convert_to_gn_str(msvc_config.msbuild_path))

    return content

def generate_environment(arch):
    msvc_config = _get_msvc_config(arch)

    e = os.environ.copy()
    e['PATH'] = str(msvc_config.msvc_bin) + ';' + e['PATH']

    return utility.generate_environment_block(e)

def generate_winsdk():
    winsdk_config = winsdk.get_latest_config()

    content = ""
    content += 'include = {}\n'.format(utility.convert_to_gn_str(winsdk_config.include_path))
    content += 'lib = {}\n'.format(utility.convert_to_gn_str(winsdk_config.lib_path))
    content += 'root = {}\n'.format(utility.convert_to_gn_str(winsdk_config.install_path))

    return content;

_add('winsdk', generate_winsdk)
_add('msvc_x86', lambda: generate_msvc('x86'))
_add('msvc_x64', lambda: generate_msvc('x64'))
_add('msvc_environment.x86', lambda: generate_environment('x86'))
_add('msvc_environment.x64', lambda: generate_environment('x64'))

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