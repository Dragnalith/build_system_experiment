#pragma once

// Platform Config

#ifndef DRGN_PLATFORM_IS_MAC
#define DRGN_PLATFORM_IS_MAC 0
#endif

#ifndef DRGN_PLATFORM_IS_WIN32
#define DRGN_PLATFORM_IS_WIN32 0
#endif

#ifndef DRGN_PLATFORM_IS_WIN64
#define DRGN_PLATFORM_IS_WIN64 0
#endif

#ifndef DRGN_PLATFORM_IS_NX
#define DRGN_PLATFORM_IS_NX 0
#endif

#ifndef DRGN_PLATFORM_IS_ORBIS
#define DRGN_PLATFORM_IS_ORBIS 0
#endif

namespace drgn {

struct Config {
};

Config getConfig();

}