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
# 9 Fev 2020
- I am thinking about how to split the configuration into cross-platform configuration. For let's define a target "platform". The compination of the OS + CPU give me a platform. The same platform can be built with different sdk compatible with that platform. For instance I can extract from the WinSDK folder a WinSDK configuration for Windows_x64, Windows_x86, or Windows_ARM. What about toolchain? Each platform has different toolchain, but several toolchain can exist for the same platform. About SDK, as for WinSDK, an SDK configuration depend on the platform, but could be compatible for different toolchain. Can we be sure that every sdk compatible for one platform is also compatible with every toolchain compatible for that platform. This hypothesis is wrong at least for visual studio, some .lib are only compatible with a particular version of visual studio.
Conclusion: SDK configuration depend on the platform and the toolchain, even if for a lot a case it will depend only on the platform.
- Toolchains are defined during the first configuration path (the one using the default toolchain), so when defining a toolchain, 'current_cpu' value is not the cpu value of the toolchain being defined but is the value of the default toolchain cpu.
# 11 Fev 2020
- For one build configuration several platform needs to be taken into account. The host platform is the platform target for buildtool and tools. buildtools are application used during the build, tool are game tools (asset editors, asset compiler, asset build system, ...). The runtime platforms are platform targets for the game runtime. There is only one host platform, but several runtime platforms for one build configuration.
- Is is possible to use a variable inside a variable name in string expansion "${variable_${sub_var_name}}"? No it does not work
- In order to build runtime target for multiple toolchain, I have a global "runtime_toolchains" which list all the toolchains you what runtime to be built for. I am iterating on the toolchain in the //src/runtime config only once.
- I have been able to specify a build output per target type (e.g buildtool, runtime, tool, ...) by creating custom target to override default one. Now there are runtime_executable, tool_executable, ... those enforce the default value of output_dir
- It is now possible to specify the version of visual studio (2017, 2019) and the version of the windows sdk you want to use.
# 15 Fev 2020
- Ninja seems to only display std::cerr when a build action has failed
# 18 Fev 2020
- I am considering how to integrate C# with GN. There are two possible ways compiling with MSBuild by generating a .csproj or compiling using Roselyn directly. Compiling with Roselyn directly seems better but then I am not sure about the integration with visual studio later. Maybe the easiest is to generate a .csproj?
- Compiling C# without WPF does not seem so hard. csc.exe is quite easy to use.
- But compiling WPF is very. It is possible to use a custom .csproj a transform it as a XAML -> BAML compiler, but then you need to create pack URI resource. I did not find documentation yet about this process. I think the easiest is to generate a .csproj file.
# 23 Fev 2020
- MSVC and .PDB file is complicated. There are no way to include pdb inside a static library. Actually .obj contain the reference of where the pdb has been stored. The lib.exe does not modify anything related to pdb, it is only gathering .obj into one .lib. Later the linker will find the .pdb by reading the .obj inside .lib file. If sometimes we see pdb file next to static lib, its because the pdb file name used for .obj is the same for every .obj and this pdb is copied next to the .lib. But it is actually complicated to compile, because several cl.exe are not allowed to touch the same .pdb file at the same time.