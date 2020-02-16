#include <filesystem>
#include <fstream>
#include <string>
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

int main(int argc, char** argv) {
    Config config = parse_arg(argc, argv);

    std::string mark;
    switch (config.platform)
    {
    case Platform::Win32:
        mark = "WIN32";
        break;
    case Platform::Win64:
        mark = "WIN64";
        break;
    case Platform::Console1:
        mark = "CONSOLE1";
        break;
    case Platform::Console2:
        mark = "CONSOLE2";
        break;
    case Platform::Mac:
        mark = "MAC";
        break;
    default:
        assert(false && "The platform is not handled");
        break;
    }

	std::ifstream input_file(config.input.string());
    std::ofstream output_file(config.output.string());
	assert(input_file.is_open() && "Cannot open the input file");

	std::string line;
	while (std::getline(input_file, line))
	{
        output_file << mark << line << '\n';
	}

    return 0;
}