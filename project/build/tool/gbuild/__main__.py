import argparse
import pathlib
import shutil
import sys

import gn
import ninja
import settings

class BuildContext:
    def __init__(self, args):
        assert(args.variant is not None)

        self.args = args
        self.variant = args.variant
        self.build_folder = settings.build_root / self.variant

def configure(args: argparse.Namespace):
    pass

def generate(ctx: BuildContext):
    print('generate (variant = {})'.format(ctx.variant))
    gn.run(['gen', ctx.build_folder, '--ide=vs'])

def build(ctx: BuildContext):
    if not ctx.build_folder.is_dir():
        print("variant '{}' was not generated yet.".format(ctx.variant))
        generate(ctx)

    print('build (variant = {})'.format(ctx.variant))
    ninja.run(['-C', ctx.build_folder])

def clean(ctx: BuildContext):
    print('clean (variant = {})'.format(ctx.variant))
    if ctx.build_folder.exists():
        shutil.rmtree(ctx.build_folder)
        print('The build folder {} has been removed.'.format(ctx.build_folder))
    else:
        print('Nothing to do.')

def configure_command(args: argparse.Namespace):
    configure(args)

def generate_command(args: argparse.Namespace):
    ctx = BuildContext(args)
    generate(ctx)

def build_command(args: argparse.Namespace):
    ctx = BuildContext(args)
    build(ctx)

def clean_command(args: argparse.Namespace):
    ctx = BuildContext(args)
    clean(ctx)

def main():
    common_parser = argparse.ArgumentParser(add_help=False)                                 
    common_parser.add_argument('--verbose', '-v', action='store_true', help='display more information about the command execution')
    
    build_context_parser = argparse.ArgumentParser(add_help=False)                                 
    build_context_parser.add_argument('--variant', nargs=1, default='debug', help='select which build option set to be used for the build')

    parser = argparse.ArgumentParser(description='The main command to build your project')
    parser.set_defaults(command=None)
    subparsers = parser.add_subparsers()

    configure_parser = subparsers.add_parser('configure', help='find environment information necessary to run the build (toolchain, sdk path, ...)', parents=[common_parser])
    configure_parser.set_defaults(command=configure_command)
    
    generate_parser = subparsers.add_parser('generate', aliases=['gen'], help='generate ninja file for a particular build variant', parents=[common_parser, build_context_parser])
    generate_parser.set_defaults(command=generate_command)

    build_parser = subparsers.add_parser('build', help='build targets of a particular build variant', parents=[common_parser, build_context_parser])
    build_parser.set_defaults(command=build_command)

    build_parser = subparsers.add_parser('clean', help='clean target and intermediate data of a particular build variant', parents=[common_parser, build_context_parser])
    build_parser.set_defaults(command=clean_command)

    
    arguments = parser.parse_args()

    if arguments.command == None:
        parser.print_help()
    else:
        if arguments.verbose:
            settings.verbose = True

        arguments.command(arguments)

if __name__ == "__main__":
    main()