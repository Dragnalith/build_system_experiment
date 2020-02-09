import sys
import os
import pathlib

import helpers.utility as util
import helpers.vstudio as vstudio

"""
Create environment file to be used with 'ninja -t msvc -e {env}'
and setup some toolchain variable for gn
"""

def main():
    if len(sys.argv) != 3:
        print('Usage:\n  setup_msvc_environment.py <vs_version> <arch>')
        sys.exit(-1)

    vs_version = sys.argv[1]
    arch = sys.argv[2]
    
    assert(vs_version in ['2017', '2019'])
    assert(arch in ['x86', 'x64'])

    msvc_config = vstudio.get_msvc_config(vs_version, arch)

    print('include = {}'.format(util.convert_to_gn_str(msvc_config.msvc_include)))
    print('lib = {}'.format(util.convert_to_gn_str(msvc_config.msvc_lib)))
    print('bin = {}'.format(util.convert_to_gn_str(msvc_config.msvc_bin)))
    print('root = {}'.format(util.convert_to_gn_str(msvc_config.msvc_path)))

if __name__ == '__main__':
    main()