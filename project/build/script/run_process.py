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

    # NOTE: Do not forget check=True, otherwise the python script will succeed even if the underlying
    # has failed
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    sys.stdout.write(stdout.decode())
    sys.stderr.write(stderr.decode())

    if (process.returncode != 0):
        raise Exception("run_process.py error: Process exit code is {}, it is not zero".format(process.returncode))

if __name__ == '__main__':
    main()