"""
Run the process given on the command line.

NOTE: This script is required because GN cannot process, only python script
"""

import sys
import subprocess

def main():
    if len(sys.argv) <= 1:
        print('Usage:\n  run_process.py <process_path> [args...]')
        sys.exit(-1)

    command = [str(x) for x in sys.argv[1:]]

    print("run_processy.py: Run the following command '{}'".format(' '.join(command)))

    subprocess.run(command)

if __name__ == '__main__':
    main()