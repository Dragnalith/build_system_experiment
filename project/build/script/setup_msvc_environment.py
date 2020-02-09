import sys
import os
import pathlib

import helpers.utility as util

"""
Create environment file to be used with 'ninja -t msvc -e {env}'
"""

def main():
    if len(sys.argv) != 3:
        print('Usage:\n  setup_msvc_environment.py <msvc_bin_path> <env>')
        sys.exit(-1)

    msvc_path = sys.argv[1]
    env_file = pathlib.Path(sys.argv[2])

    e = os.environ.copy()
    e['PATH'] = msvc_path + ';' + e['PATH']
    util.write_environment_block(env_file, e)

if __name__ == '__main__':
    main()