#include <drgn/Engine.h>
#include <drgn/Config.h>

#include <drgn/generated/calculator.service.h>

#include <string>
#include <sstream>
namespace drgn
{

    int getVersion()
    {
        return 2020;
    }
    const char *getName()
    {
        return "DRGN Engine";
    }

    std::string getComputerServiceList()
    {
        std::stringstream stream;
        for (auto name : ServiceInfo) {
            stream << name << ", ";
        }
        return stream.str();
    }

    const char *getPlatformName()
    {
#if DRGN_PLATFORM_IS_WIN64
        return "Win64";
#elif DRGN_PLATFORM_IS_WIN32
        return "Win32";
#elif DRGN_PLATFORM_IS_MAC
        return "Mac";
#elif DRGN_PLATFORM_IS_CONSOLE1
        return "Console1";
#elif DRGN_PLATFORM_IS_CONSOLE2
        return "Console2";
#endif
    }

} // namespace drgn