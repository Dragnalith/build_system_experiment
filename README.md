# Features

- Multiplatform build system: 
  - build for any platform as part as the same build graph
  - reuse tool from one platform to build for another
- Compatible with code generator:
  - you can create code generator build rule
  - code generator tool can be built as dependency of code generator build rule
- Compatible with runtime data compilation
  - application can have data dependency
  - custom buile rule can be added to convert your data (texture, font, shader)
- Compatible with C# and 
- Build output folder independent from source tree
- Fine grain build flag (per build output folder)
- Integration with Visual Studio