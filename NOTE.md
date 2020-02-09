# 4 Jan 2020:
- Actually I will try to use real compiler to be able to compile
real C++ code instead of mock compiler.
- Setup compilation with both GCC and Clang on OS X
- Setup compilation with bash script and ninja
# 5 Jan 2020
- I think I should also consider fastbuild and premake. Those build system may
be able to compile for several platform at the same time.
- Currently I am giving up testing CMake because it does not support building
multiple toolchain at the same time. This scenario is important because different
platform may need the same tool (some texture converter, same code generator) and I do not want to rebuild it for every target platform.
- With GN, the meaning of target_os and current_os is unclear (as well as target_cpu and current_cpu). It seems useful when you want to point to a particular target when the build user want to say "I want to build for that platform". But when the build user want to build for multiple platform at the same time, it is unclear what should be done.
- Actually I found the meaning. When you refer to a target using another tool chain (e.g //my/target:name(//other/toolchain)), if it is not the case, GN will run the related build file again with the new toolchain, including BUILDCONFIG.gn. But instead of using original argument, it will use the argument override in the toolchain definition. Whatever the toolchain context you are running, host_os always means the platform from which GN is running and target_os always mean the target_os value which has been given as build argument. The only value which could change when a build file is call for another toolchain is the current_os value. (note: it seems to be the same idea for host_cpu, target_cpu, and current_cpu)
- I have successfully setup GN so it can build multiple target at the same time and always put the output on the same folder whatever the "target_os" value you have given.
- I have just realized it was not possible to add a custom toolchain on premake with Ninja.
# 7 Fev 2020:
- Actually I wonder actually why I thought Ninja generator for premake is not compatible with custom toolchain. In particular is C# compatible with ninja generator for premake?
- I have added binary for ninja.exe and gn.exe
- Compiling from command line with msvc in not convenient because you need a special environment to be setup.
- It seems that actually special environment is not required except PATH. Indeed, DLL required by msvc are needed to be on the PATH before the compiler or linker run. Other include and lib variable can be set on the command line.
- When running cl.exe through 'ninja -t msvc -e {env} -- cl.exe ' I got an error message because it cannot create temporary file. 'ninja -t msvc -e {env}' execute a process with the content of {env} as environment variable instead of the current one. This file format is a bit special, and I have discovered that PATH is not enough to run correctly cl.exe (and even python). It seems a lot of program  expect some system environment variable, but I am not sure which one.
# 8 Fev 2020
- Python is a pain to deal with module. I have discovered it was not very possible to use a file as top-level script and as a module at the same time. I wonder why __name__=='__main__' trick is used so often then. Indeed import path does not work the same depending if you are a top level script or a python module.
- I have made ninja worked on windows. The biggest problem is that MSVC require some environment variable to work properly and ninja does not let you setup environment variable for a rule. You need to use the 'ninja -t msvc -e {env} --' trick which require use to generate somehow the {env} file.
- I was thinking about how to integrate C# to 'gn'. My first idea is to generate an msbuild file and use msbuild as an atomic build action. In theory it should work, but then I do not have any idea on how to integrate C# into the generated visual studio solution. If I do an nmake target as for C++ project the UX may not be that great, if I include the generated .csproj file, building this file from Visual Studio will not use ninja, so it won't build dependencies.