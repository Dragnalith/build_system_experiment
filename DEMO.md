# Presentation

- Goal Of Phoenix:
- Future Work: 
  - Incredibuild
  - Real platform toolchain
  - Console platform visual studio integration

# Demo

## Basic Compilation
- Compile everything
  $ ..\bin\win\gn.exe gen _out
  $ ..\bin\win\ninja.exe -C _out
- Run:
  - Runtime
  - Tool
  - Tool UI
- Check data
  - Texture
  - Image

## Compile everything necessary, but only what is necessary

- Destroy everything and recompile only one platform
  $ ..\bin\win\ninja.exe -C _out -t clean & rmdir /Q /S _out\out
  $ ..\bin\win\ninja.exe -C _out out/runtime/Win64/bin/runtime_app.exe
    - check only the platform folder has been compiled
    - check all its data has been compiled but not other platform
- Destroy everything and recompile one shader
    - check only shader compiler and shader has been recompiled
  $ ..\bin\win\ninja.exe -C _out -t clean & rmdir /Q /S _out\out
  $ ..\bin\win\ninja.exe -C _out out/runtime/Win64/data/shaders/system/system.bin

## Incremental build works with code generator

- Recompile everything
- Change service file and check recompiling runtime will re-generated code
  * Open service file
  * Open generated file
- Change code generator code and check recompiing runtime will recompile code generator and re-generate code
  * Open rpc_generate source file

## Asset data are compiled as runtime dependency


- Change data and check recompiling runtime will recompile
    - recompile only one runtime and check only data for that runtime has been recompiled
    $ ..\bin\win\ninja.exe -C _out out/runtime/Win64/bin/runtime_app.exe
- Change compiler code and check recompiling runtime will recompile shader

## Build folder

csharp_enabled=true
buildtool_optimized=true
runtime_optimized=true
tool_optimized=true
assert_enabled=true
log_enabled=true

- Configure another build folder, notify build is independent from build output folder
- Configure another folder with another preset
- Reconfigure the same folder changing build setting
  - Check only affected artefact are recompiled

## Visual Studio

- Open visual studio solution and verify it works as expected
  - compile
  - run application
  - add break point
  - run WPF application