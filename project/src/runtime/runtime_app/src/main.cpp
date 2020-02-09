#include <drgn/Engine.h>

#include <iostream>

int main() {
    std::cout << "I am the runtime " << drgn::getName() << " version " << drgn::getVersion() << '\n';

    return 0;
}