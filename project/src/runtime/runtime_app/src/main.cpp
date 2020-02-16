#include <drgn/Engine.h>

#include <iostream>

int main() {
    std::cout << "I am the runtime " << drgn::getName() << " version " << drgn::getVersion() << '\n';
    std::cout << "I am running under the following platform: " << drgn::getPlatformName() << '\n';
    std::cout << "The computer service name is : " << drgn::getComputerServiceName() << '\n';

    return 0;
}