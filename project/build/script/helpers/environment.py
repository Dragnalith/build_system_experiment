import platform
import sys
import pathlib
import helpers.utility as util

class UnknownSystem(Exception):
    """
        The following script run on an unknown system
    """
    pass

class Environment:
    """
        This is a helper class to be used as a global.
        It centralize the repository configuration (filetree, etc.)
        So other script can only depend on variable
    """
    def __init__(self):
        self.root = util.find_root_mark('RootMark')
        self.system = platform.system()

        if self.system == 'Windows':
            self.bin = self.root / 'bin/win'
            self.ninja = self.bin / 'ninja.exe'
            self.gn = self.bin / 'gn.exe'
            self.vswhere = self.bin / 'vswhere.exe'
        else:
            raise UnknownSystem('The "{}" system is not supported'.format(self.system))


path = Environment()

def test_print():
    print('Root={}'.format(path.root))
    print('Ninja={}'.format(path.ninja))
    print('GN={}'.format(path.gn))
    print('VSWhere={}'.format(path.vswhere))
