import pathlib
import subprocess
import helpers.environment as env

vs_version_map = {
    '2017' : 15,
    '2019' : 16
}

class MSVCConfig:
    """
        Gather information about a particular MSVC distribution
    """
    def __init__(self, vs_version, arch):
        assert(arch in ['x86', 'x64'])

        self.version = vs_version
        self.arch = arch
        self.install_path = get_vs_install_path(vs_version)
        self.msbuild_path = get_msbuild_path(vs_version)
        self.msvc_path = get_msvc_default_path(vs_version)
        self.msvc_bin = self.msvc_path / 'bin/Host{arch}/{arch}'.format(arch=arch)
        self.msvc_include = self.msvc_path / 'include'
        self.msvc_lib = self.msvc_path / 'lib/{arch}'.format(arch=arch)

        self.install_path.resolve()
        self.msvc_path.resolve()
        self.msvc_bin.resolve()
        self.msvc_include.resolve()
        self.msvc_lib.resolve()

    def __str__(self):
        result = 'Visual Studio {} Config for {}\n'.format(self.version, self.arch)
        result += 'install_path={}\n'.format(self.install_path)
        result += 'msvc_path={}\n'.format(self.msvc_path)
        result += 'msvc_bin={}\n'.format(self.msvc_bin)
        result += 'msvc_include={}\n'.format(self.msvc_include)
        result += 'msvc_lib={}\n'.format(self.msvc_lib)

        return result

def run_vswhere(args):
    """
        Helper to run vswhere.exe in order to find information about
        local visual studio installation.
    """
    command = [env.path.vswhere, '-nologo'] + args
    output = subprocess.run(command, stdout=subprocess.PIPE)
    
    return output.stdout.decode().strip("\r\n").strip('\r').strip('\n')

def get_msbuild_path(vs_version):
    """
        return the install path of a Visual Studio installation.
        'vs_version' can be "2017" or "2019"
    """
    assert(vs_version in vs_version_map)
    v = vs_version_map[vs_version]
    args = ['-version', '[{},{}]'.format(v, v+1), '-find', 'MSBuild\**\Bin\MSBuild.exe']

    output = run_vswhere(args)
    if len(output) > 0:
        return pathlib.Path(output)
    else:
        return None

def get_vs_install_path(vs_version):
    """
        return the install path of a Visual Studio installation.
        'vs_version' can be "2017" or "2019"
    """
    assert(vs_version in vs_version_map)
    v = vs_version_map[vs_version]
    args = ['-version', '[{},{}]'.format(v, v+1), '-property', 'installationPath']

    output = run_vswhere(args)
    if len(output) > 0:
        return pathlib.Path(output)
    else:
        return None

def get_msvc_default_version(install_path):
    """
        return the default msvc version of the visual studio distribution given as argument.
        (For a same visual studio distribution, several msvc can be installed, I am expecting
        it to return the most recent one)
    """
    version_file = install_path / 'VC/Auxiliary/Build/Microsoft.VCToolsVersion.default.txt'

    if not version_file.exists():
        return None

    with open(version_file, 'r') as file:
        return file.read().strip("\r\n").strip('\n').strip('\r')

def get_msvc_default_path(vs_version):
    """
        return the path to an MSVC distribution for a particular version of visual studio.
        (a same version of visual studio can contain different MSVC distribution)
    """
    install_path = get_vs_install_path(vs_version)

    if install_path is None:
        return None

    default_version = get_msvc_default_version(install_path)
    msvc_path = install_path / 'VC/Tools/MSVC' / default_version

    if msvc_path.exists():
        return msvc_path
    else:
        return None


def get_msvc_config(vs_version, arch):
    return MSVCConfig(vs_version, arch)

def test_print():
    configs = [
        get_msvc_config('2017', 'x86'),
        get_msvc_config('2017', 'x64'),
        get_msvc_config('2019', 'x86'),
        get_msvc_config('2019', 'x86')
    ]

    for c in configs:
        print(c)
