import pathlib

default_install_path = pathlib.Path('C:/Program Files (x86)/Windows Kits/10')

class WinSdkConfig:
    def __init__(self, version):
        self.version = version
        self.install_path = default_install_path
        self.include_path = self.install_path / 'Include' / self.version
        self.lib_path = self.install_path / 'Lib' / self.version
        self.install_path.resolve()
        self.include_path.resolve()
        self.lib_path.resolve()

        assert(self.include_path.exists())
        assert(self.lib_path.exists())

    def __str__(self):
        result = 'WinSDK Config version: {}\n'.format(self.version)
        result += 'install_path={}\n'.format(self.install_path)
        result += 'winsdk_include_path={}\n'.format(self.include_path)
        result += 'winsdk_lib_path={}\n'.format(self.lib_path)

        return result

def get_version_list():
    if not default_install_path.exists() or not default_install_path.is_dir():
        return set()

    include = default_install_path / 'Include'
    include_versions = set()
    for f in include.iterdir():
        include_versions.add(f.name)

    include = default_install_path / 'Lib'
    lib_versions = set()
    for f in include.iterdir():
        lib_versions.add(f.name)

    return include_versions & lib_versions

def get_latest_version():
    versions = get_version_list()
    
    if len(versions) == 0:
        return None

    expanded_versions = [x.split('.') for x in versions]
    sorted_versions = ['.'.join(k) for k in sorted(expanded_versions, reverse=True)]
    
    assert(len(sorted_versions) > 0)

    return sorted_versions[0]

def get_latest_config():
    return WinSdkConfig(get_latest_version())

def test_print():
    print(get_latest_config())
