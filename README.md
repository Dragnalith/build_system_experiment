# Purpose

The purpose of that repository is to evaluate different build system.

For that I am creating the mock 'project' folder and will configure its build with different build system.

The build system I have in mind at first:
- GN
- Fastbuild

Then maybe:
- Bazel (but it does not deal with dynamic dependencies)
- Premake (but is it possible to easily extend the ninja generator?)
- Meson (but is it possible to add new toolchain, new language, and build for multiple platform with the same buildgraph)

Won't be tested:
- CMake, because it is not possible to generate a build graph for several platform at the same time