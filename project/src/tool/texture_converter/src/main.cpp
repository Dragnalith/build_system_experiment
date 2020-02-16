#include "stb_image.h"
#include "stb_image_write.h"

#include <filesystem>
#include <string>
#include <vector>
#include <cmath>
#include <stdint.h>
#include <assert.h>

enum class Platform {
    Win64,
    Win32,
    Mac,
    Console1,
    Console2
};

struct Config {
    Platform platform;
	std::filesystem::path input;
	std::filesystem::path output;
};

Config parse_arg(int argc, char** argv) {
	assert(argc > 0);

	std::vector<std::string> args;

	Config config;
    std::string platform_name;
    
	for (int i = 1; i < argc; i++) {
		args.push_back(argv[i]);
	}

	for (int i = 0; i < args.size(); i++) {
		auto arg = args[i];
		if (arg == "-o") {
			i += 1;
			config.output = args[i];
		}
		else if (arg == "--platform") {
			i += 1;
            platform_name = args[i];
		}
		else {
			config.input = arg;
		}
	}

    if (platform_name == "Win32") {
        config.platform = Platform::Win32;
    } else if (platform_name == "Win64") {
        config.platform = Platform::Win64;
    } else if (platform_name == "Mac") {
        config.platform = Platform::Mac;
    } else if (platform_name == "Console1") {
        config.platform = Platform::Console1;
    } else if (platform_name == "Console2") {
        config.platform = Platform::Console2;
    } else {
        assert(false && "Platform is unknown");
    }

	assert(args.size() > 3);

	assert(std::filesystem::exists(config.input) && "input file does not exist");

	return config;
}

const int win64_mark[8*8] = {
    1, 1, 1, 1, 0, 1, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 1,
    1, 1, 1, 1, 0, 1, 1, 1,
    1, 0, 0, 1, 0, 0, 0, 1,
    1, 0, 0, 1, 0, 0, 0, 1,
    1, 0, 0, 1, 0, 0, 0, 1,
    1, 1, 1, 1, 0, 0, 0, 1
};
const int win32_mark[8*8] = {
    1, 1, 1, 1, 0, 1, 1, 1,
    0, 0, 0, 1, 0, 0, 0, 1,
    0, 0, 0, 1, 0, 0, 0, 1,
    1, 1, 1, 1, 0, 1, 1, 1,
    0, 0, 0, 1, 0, 1, 0, 0,
    0, 0, 0, 1, 0, 1, 0, 0,
    0, 0, 0, 1, 0, 1, 0, 0,
    1, 1, 1, 1, 0, 1, 1, 1
};
const int console1_mark[8*8] = {
    0, 0, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 0
};
const int console2_mark[8*8] = {
    0, 0, 1, 1, 1, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 1, 1, 1, 1, 1, 0,
    0, 0, 1, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 1, 0
};
const int mac_mark[8*8] = {
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 1, 0, 0, 0, 0, 1, 1,
    1, 0, 1, 0, 0, 1, 0, 1,
    1, 0, 0, 1, 1, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 1
};

int main(int argc, char** argv) {
    Config config = parse_arg(argc, argv);

    int n = 4;
    int x, y, c;
    uint8_t* data = stbi_load(config.input.string().c_str(), &x, &y, &c, n);

    int point_size = 16;
    const int size_x = std::min(x, 8 * point_size);
    const int size_y = std::min(y, 8 * point_size);
    
    const int* mark = win64_mark;

    switch (config.platform)
    {
    case Platform::Win32:
        mark = win32_mark;
        break;
    case Platform::Win64:
        mark = win64_mark;
        break;
    case Platform::Console1:
        mark = console1_mark;
        break;
    case Platform::Console2:
        mark = console2_mark;
        break;
    case Platform::Mac:
        mark = mac_mark;
        break;
    default:
        assert(false && "The platform is not handled");
        break;
    }

    for (int i = 0; i < size_x; i++) {
        for (int j = 0; j < size_y; j++) {
            if (mark[i / point_size + (j / point_size) * 8] == 1) {
                uint8_t* pixel = &data[i * n + j * x * n];
                for (int k = 0; k < std::min(3, n); k++) {
                    pixel[k] = 0;
                }
                if (n == 4) {
                    pixel[3] = 255;
                }
            }
        }
    }

    stbi_write_bmp(config.output.string().c_str(), x, y, n, data);

    stbi_image_free(data);
    return 0;
}