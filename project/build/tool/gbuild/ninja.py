import subprocess

import settings

def run(args):
    command = [str(settings.ninja)] + args

    print('Run Ninja:')
    if settings.verbose:
        print('({})'.format(' '.join([str(x) for x in command])))

    return subprocess.run(command).returncode