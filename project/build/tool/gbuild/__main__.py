import argparse
import pathlib
import sys

import gn
import ninja
import settings
import environment
import utility

class BuildContext:
    def __init__(self, args):
        assert(args.variant is not None)

        if args.variant_file is not None:
            path = pathlib.Path(args.variant_file)
            assert path.exists(), "The variant file {} does not exist.".format(path)
            self.variant = path.stem
            self.build_folder = settings.build_root / self.variant
            self.variant_file = path
        else:
            assert args.variant is not None
            self.variant = args.variant
            self.build_folder = settings.build_root / self.variant
            if self.variant in settings.builtin_variants:
                self.variant_file = settings.variant_folder / self.variant
            else:
                self.variant_file = pathlib.Path((self.build_folder / settings.variant_path_filename).read_text())

        settings.last_variant.write_text(self.variant)

        self.args = args
        self.verbose = args.verbose
        self.build_folder = settings.build_root / self.variant
        self.variant_path_file = self.build_folder / settings.variant_path_filename

        if args.targets is not None:
            self.targets = [x.strip('/') for x in args.targets]
        else:
            self.targets = []

def configure(args: argparse.Namespace):
    print('configure')
    environment.generate();

def generate(ctx: BuildContext):
    if not environment.all_exists():
        print("environment was not generated, so run 'configure'.")
        configure(ctx.args)

    gn_args = ctx.variant_file.read_text()

    print('generate (variant = {})'.format(ctx.variant))
    args = ['gen', ctx.build_folder, '--ide=vs', '--args={}'.format(gn_args)]

    if ctx.verbose:
        args.append('--verbose')
    exitcode = gn.run(args)
    assert exitcode == 0, "generate has failed (GN execution return {}".format(exitcode)

    ctx.variant_path_file.write_text(str(ctx.variant_file.absolute()))

def list_options(ctx: BuildContext):
    if not ctx.build_folder.is_dir():
        print("variant '{}' build file are not generated, so run 'generate'.".format(ctx.variant))
        generate(ctx)

    print('list options (variant = {})'.format(ctx.variant))
    exitcode = gn.run(['args', ctx.build_folder, '--list'])
    assert exitcode == 0, "list option has failed (GN execution return {}".format(exitcode)

def build(ctx: BuildContext):
    if not ctx.build_folder.is_dir():
        print("variant '{}' build file are not generated, so run 'generate'.".format(ctx.variant))
        generate(ctx)

    print('build (variant = {})'.format(ctx.variant))

    if len(ctx.targets) > 0:
        print("Build the following target:")
        for t in ctx.targets:
            print('    //{}'.format(t))

    args = ['-C', ctx.build_folder]
    if ctx.verbose:
        args.append('--verbose')

    args += ctx.targets

    ninja.run(args)

def clean(ctx: BuildContext, all = False):
    if all:
        print('clean all')
        if settings.build_root.exists():
            if utility.clean_dir(settings.build_root):
                print('The build folder {} has been deleted.'.format(settings.build_root))
            else:
                print('The build folder {} could not been deleted. Some files remain'.format(ctx.build_folder))
        else:
            print('Nothing to do.')
    else:
        print('clean (variant = {})'.format(ctx.variant))

        if len(ctx.targets) > 0:
            print("Clean the following target:")
            for t in ctx.targets:
                print('    //{}'.format(t))

            args = ['-C', ctx.build_folder, '-tclean']
            if ctx.verbose:
                args.append('--verbose')

            args += ctx.targets

            ninja.run(args)
        else:
            if ctx.build_folder.exists():
                if utility.clean_dir(ctx.build_folder):
                    print('The build folder {} has been deleted.'.format(ctx.build_folder))
                else:
                    print('The build folder {} could not been deleted. Some files remain'.format(ctx.build_folder))
            else:
                print('Nothing to do.')

def configure_command(args: argparse.Namespace):
    configure(args)

def generate_command(args: argparse.Namespace):
    ctx = BuildContext(args)
    generate(ctx)

def list_options_command(args: argparse.Namespace):
    ctx = BuildContext(args)
    list_options(ctx)

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
    build_context_parser.add_argument('targets', nargs='*', action='store', help='list of targets to be built.')
    variant_group = build_context_parser.add_mutually_exclusive_group()
    variant_group.add_argument('--variant', default=settings.default_variant, choices=settings.variants, help='select which build option set to be used for the build (from existing build file')
    variant_group.add_argument('--variant_file', help='select which build option set to be used for the build')

    parser = argparse.ArgumentParser(description='The main command to build your project')
    parser.set_defaults(command=None)
    subparsers = parser.add_subparsers()

    configure_parser = subparsers.add_parser('configure', help='find environment information necessary to run the build (toolchain, sdk path, ...).', parents=[common_parser])
    configure_parser.set_defaults(command=configure_command)
    
    generate_parser = subparsers.add_parser('generate', aliases=['gen'], help='generate ninja file for a particular build variant.', parents=[common_parser, build_context_parser])
    generate_parser.set_defaults(command=generate_command)

    list_options_parser = subparsers.add_parser('list_options', aliases=['gen'], help='list the build option available.', parents=[common_parser, build_context_parser])
    list_options_parser.set_defaults(command=list_options_command)

    build_parser = subparsers.add_parser('build', help='build targets of a particular build variant.', parents=[common_parser, build_context_parser])
    build_parser.set_defaults(command=build_command)

    clean_parser = subparsers.add_parser('clean', help='clean target and intermediate data of a particular build variant.', parents=[common_parser, build_context_parser])
    clean_parser.add_argument('--all', action='store_true', help='Clean all variant and environment (delete all {}).'.format(settings.build_root))
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