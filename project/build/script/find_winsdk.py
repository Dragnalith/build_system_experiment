import sys
import os
import pathlib

import helpers.environment as env
import helpers.utility as util
import helpers.winsdk as winsdk
import helpers.vstudio as vstudio

"""
Setup winsdk variable for gn
"""

def main():
    if len(sys.argv) > 1:
        winsdk_config = winsdk.get_config(sys.argv[1])
    else:
        winsdk_config = winsdk.get_latest_config()

    print('include = {}'.format(util.convert_to_gn_str(winsdk_config.include_path)))
    print('lib = {}'.format(util.convert_to_gn_str(winsdk_config.lib_path)))
    print('root = {}'.format(util.convert_to_gn_str(winsdk_config.install_path)))

if __name__ == '__main__':
    main()