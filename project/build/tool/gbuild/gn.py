import subprocess

import settings

def run(args):
    command = [str(settings.gn)] + args

    print("Run GN:")
    if settings.verbose:
        print('({})'.format(' '.join(command)))

    subprocess.run(command)