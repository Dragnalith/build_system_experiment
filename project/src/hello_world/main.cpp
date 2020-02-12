#include <iostream>

#if defined(__clang__)
const char* g_CompilerName = "Clang";
#elif defined(__GNUC__)
const char* g_CompilerName = "GCC";
#elif defined(_WIN64) && _WIN64
const char* g_CompilerName = "Win64";
#elif defined(_WIN32) && _WIN32
const char* g_CompilerName = "Win32";
#else
const char* g_CompilerName = "Undefined Compiler";
#endif

int main() {
    std::cout << "Hello World from compiler" << g_CompilerName << "\n";
    
    return 0;
}
