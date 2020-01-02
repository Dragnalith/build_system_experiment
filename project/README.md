The 'project' represent the source tree we want to build. In a real scenario it would
be the root directory of the repository.

See below the output directory we want to achieve:
```
build_output/
+-- buildtool/
    +-- rpc_generator.exe
    +-- reflection_data_generator.exe
+-- tool/
|   +-- LevelEditor.exe
|   +-- AssetBuidlSystem.exe
|   +-- TextureConverter.exe
|   +-- MaterialConverter.exe
|   +-- MeshConverter.exe
|   +-- ShaderCompiler.exe
|   +-- much more...
+-- Win64/
|   +-- data/
|   |   +-- shader/
|   |   |   +-- system_shader1.bin
|   |   |   +-- system_shader2.bin
|   |   |   +-- much more ...
|   |   +-- asset/
|   |   |   +-- default_texture.bin
|   |   |   +-- debug_font.ttf
|   |   +-- config.ini
|   |   +-- much more ...
|   |-- bin/
|   |   +-- EngineRuntime.exe
|   |   +-- EngineRuntime.pdb
|   |-- lib/
|       +-- Engine.lib
|       +-- Engine.pdb
+-- <Console Vendor 1>/
|   +-- data/ # data required to run
|   |   +-- shader/
|   |   |   +-- system_shader1.bin
|   |   |   +-- system_shader2.bin
|   |   |   +-- much more ...
|   |   +-- asset/
|   |   |   +-- default_texture.bin
|   |   |   +-- debug_font.ttf
|   |   +-- config.ini
|   |   +-- much more ...
|   |-- bin/
|   |   +-- EngineRuntime.elf
|   |-- lib/
|       +-- Engine.a
+-- <Console Vendor 2>/
    +-- ...
```
