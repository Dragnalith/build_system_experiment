import sys
import helpers
import argparse

def configure(args):
    print('configure')

def generate(args):
    print('generate')

def build(args):
    print('build')
    print(args)

def main():
    parser = argparse.ArgumentParser(description='The main command to build your project')
    parser.set_defaults(command=None)
    subparsers = parser.add_subparsers()

    configure_parser = subparsers.add_parser('configure', help='help configure')
    configure_parser.set_defaults(command=configure)
    
    generate_parser = subparsers.add_parser('generate', aliases=['gen'], help='help generate')
    generate_parser.set_defaults(command=generate)

    build_parser = subparsers.add_parser('build', help='help build')
    build_parser.add_argument('--preset', nargs=1)
    build_parser.add_argument('targets', nargs='*')
    build_parser.set_defaults(command=build)

    
    arguments = parser.parse_args()

    if arguments.command == None:
        parser.print_help()
        return
    else:
        arguments.command(arguments)

if __name__ == "__main__":
    main()