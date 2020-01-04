#include <iostream>

#if defined(__clang__)
const char* g_CompilerName = "Clang";
#elif defined(__GNUC__)
const char* g_CompilerName = "GCC";
#else
const char* g_CompilerName = "Undefined Compiler";
#endif

int main() {
    std::cout << "Hello World from " << g_CompilerName << "\n";
    return 0;
}