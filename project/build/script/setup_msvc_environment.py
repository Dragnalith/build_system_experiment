import sys
import os
import pathlib

import helpers.environment as env
import helpers.utility as util
import helpers.vstudio as vstudio

"""
Create environment file to be used with 'ninja -t msvc -e {env}'
and setup some toolchain variable for gn
"""

def main():
    if len(sys.argv) != 4:
        print('Usage:\n  setup_msvc_environment.py <vs_version> <arch> <env>')
        sys.exit(-1)

    vs_version = sys.argv[1]
    arch = sys.argv[2]
    env_file = pathlib.Path(sys.argv[3])
    
    assert(vs_version in ['2017', '2019'])
    assert(arch in ['x86', 'x64'])

    msvc_config = vstudio.get_msvc_config(vs_version, arch)

    e = os.environ.copy()
    e['PATH'] = str(msvc_config.msvc_bin) + ';' + e['PATH']
    util.write_environment_block(env_file, e)

    print('include = {}'.format(util.convert_to_gn_str(msvc_config.msvc_include)))
    print('lib = {}'.format(util.convert_to_gn_str(msvc_config.msvc_lib)))
    print('bin = {}'.format(util.convert_to_gn_str(msvc_config.msvc_bin)))
    print('root = {}'.format(util.convert_to_gn_str(msvc_config.msvc_path)))
    print('env = {}'.format(util.convert_to_gn_str(env_file)))

if __name__ == '__main__':
    main()