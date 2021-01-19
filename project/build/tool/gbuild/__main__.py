import argparse
import pathlib
import shutil
import sys

import gn
import ninja
import settings
import environment

class BuildContext:
    def __init__(self, args):
        assert(args.variant is not None)

        self.args = args
        self.verbose = args.verbose
        self.variant = args.variant
        self.build_folder = settings.build_root / self.variant

def configure(args: argparse.Namespace):
    print('configure')
    environment.generate();

def generate(ctx: BuildContext):
    if not environment.all_exists():
        print("environment was not generated, so run 'configure'.")
        configure(ctx.args)

    print('generate (variant = {})'.format(ctx.variant))
    exitcode = gn.run(['gen', ctx.build_folder, '--ide=vs'])
    assert exitcode == 0, "generate has failed (GN execution return {}".format(exitcode)

def build(ctx: BuildContext):
    if not ctx.build_folder.is_dir():
        print("variant '{}' build file are not generated, so run 'generate'.".format(ctx.variant))
        generate(ctx)

    print('build (variant = {})'.format(ctx.variant))

    args = ['-C', ctx.build_folder]
    if ctx.verbose:
        args.append('--verbose')

    ninja.run(args)

def clean(ctx: BuildContext, all = False):
    print('clean (variant = {})'.format(ctx.variant))
    if all:
        if settings.build_root.exists():
            shutil.rmtree(settings.build_root)
            print('The build folder {} has been deleted.'.format(settings.build_root))
        else:
            print('Nothing to do.')
    else:
        if ctx.build_folder.exists():
            shutil.rmtree(ctx.build_folder)
            print('The build folder {} has been deleted.'.format(ctx.build_folder))
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
    clean(ctx, args.all)

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

    clean_parser = subparsers.add_parser('clean', help='clean target and intermediate data of a particular build variant', parents=[common_parser, build_context_parser])
    clean_parser.add_argument('--all', action='store_true', help='Clean all variant and environment (delete all {})'.format(settings.build_root))
    clean_parser.set_defaults(command=clean_command)

    
    arguments = parser.parse_args()

    if arguments.command == None:
        parser.print_help()
    else:
        if arguments.verbose:
            print('Verbose logger is enabled.')
            settings.verbose = True

        arguments.command(arguments)

if __name__ == "__main__":
    main()