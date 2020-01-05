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
may need the same tool (some texture converter, same code generator) and I do not
want to rebuild it for every target platform.
- With GN, the meaning of target_os and current_os is unclear (as well as target_cpu
and current_cpu). It seems useful when you want to point to a particular target when
the build user want to say "I want to build for that platform". But when the build user
want to build for multiple platform at the same time, it is unclear what should be done.
- Actually I found the meaning. When you refer to a target using another tool chain (e.g //my/target:name(//other/toolchain)), if it is not the case, GN will run the related build file again with the new toolchain, including BUILDCONFIG.gn.But instead of using original argument, it will use the argument override in the toolchain definition. Whatever the toolchain context you are running, host_os always means the platform from which GN is running and target_os always mean the target_os value which has been given as build argument. The only value which could change when a build file is call for another toolchain is the current_os value. (note: it seem idea for host_cpu, target_cpu, and current_cpu)
- I have successfully setup GN so it can build multiple target at the same time and always put the output on the same folder whatever the "target_os" value you have given.
- I have just realized it was not possible to add a custom toolchain on premake with Ninja.