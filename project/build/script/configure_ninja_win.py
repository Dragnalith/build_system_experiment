"""
Configure the build for the raw ninja file under build/gn/ninja/win/build.ninja

In short it finds MSVC and Windows SDK and generate data to be used by ninja during
the build
"""

import os
import helpers.environment as env
import helpers.utility as util
import helpers.winsdk as winsdk
import helpers.vstudio as vstudio

build_dir = env.path.root / 'out/build-ninja'
env_x64 = build_dir / 'env.x64'
env_x86 = build_dir / 'env.x86'
ninja_config = build_dir / 'config.ninja'
environment_variable = os.environ.copy()

msvc_x86 = vstudio.get_msvc_config('2017', 'x86')
msvc_x64 = vstudio.get_msvc_config('2017', 'x64')

winsdk_config = winsdk.get_latest_config()

def generate_env_file(env_path, msvc_config):
    e = environment_variable.copy()
    e['PATH'] = str(msvc_config.msvc_bin) + ';' + e['PATH']
    util.write_environment_block(env_path, e)

generate_env_file(env_x64, msvc_x64)
generate_env_file(env_x86, msvc_x86)

assert(msvc_x86.msvc_path == msvc_x64.msvc_path)
conf = {
    'msvc_dir' : str(msvc_x86.msvc_path),
    'winsdk_include' : str(winsdk_config.include_path),
    'winsdk_lib' : str(winsdk_config.lib_path)
}

util.write_ninja_file(ninja_config, conf)