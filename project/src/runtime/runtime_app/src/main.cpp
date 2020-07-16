#include <drgn/Engine.h>

#include <iostream>

constexpr bool log_enabled = DRGN_LOG_ENABLED;
constexpr bool assert_enabled = DRGN_ASSERT_ENABLED;

int main() {
#ifndef DRGN_DEBUG
    std::cout << "Optimized version" << '\n';
#else 
    std::cout << "Debug version" << '\n';
#endif
    std::cout << "Log enabled: " << (log_enabled ? "true" : "false") << '\n';
    std::cout << "Assert enabled: " << (assert_enabled ? "true" : "false") << '\n';
    std::cout << "I am the runtime " << drgn::getName() << " version " << drgn::getVersion() << '\n';
    std::cout << "I am running under the following platform: " << drgn::getPlatformName() << '\n';
    std::cout << "The computer service list is : " << drgn::getComputerServiceList() << '\n';

    return 0;
}