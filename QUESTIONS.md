# Base Research

- Is it possible to organize the build output tree however you want?
Can you choose the destination of your build artifact. Can you organize the layout yourself?
- How do you reference a particular build artifact?
The build tool can rebuild a particle artifact, how do you reference this artifact on the
build command line? Is is a path? Relative path? Relative to what?
- Does it work with glob?
If you build configuration is defined with glob pattern it means it has to re-evalute
the filesystem to update the build graph every a build is run. How does the build system
handle that scenario?
- Can it compile multiple platform in one build?
You may want to build for several target platform at the same time using a cross-compiler.
How does the build system handle that?
- Is it possible to handle different toolchain?
- Can it handle build variant at the same time?
The build can be configured with different option
- Does the build system handle custom rule/custom language?
Can you add code generator, shader compiler, asset converter, etc?
- Does rule can depends on data?
There are some build artifact which are required to run an executable, but not to build it. Is it possible to define those kind of dependencies?
- Does rule and custom rule inherit from dependency configuration?
Configuration like define, include directory, libraries for link, etc.
- Does the build system handle dynamic dependencies?
for build action which has dynamic dependencies, how is it injected back into the build graph?
- Is it possible for the build to handle dynamic output?
Some tool generate more than one file. For instance cl.exe will compile and generate executable and .pdb file. Some code generator may build a lot of file
- Can you query the build graph?
It is convenient to understand where come from a particular configuration, or maybe do we have a particular dependency, ...
- Does it support remote build?

# Advanced Research

- Is it possible to build C++ for multiple platform?
- Is it possible to build C#?
- Is is possible to build WPF?
- Is it possible for the build system to handle test?
- Is it possible to define runfile dependencies?
The simple is the runfile directory is shared among all executable, but in theory this folder can be different for every executable. Is it possible to go one step further and manage runfile per target instead of globally?
NOTE: It seems that the fact a runfile needs to be generated is independent from the fact it is required to run the target. "runfile" is just a list of file required to run the target, and maybe a mapping of where the file should be. If the file needs to be generated it has to be done in a prior step.

