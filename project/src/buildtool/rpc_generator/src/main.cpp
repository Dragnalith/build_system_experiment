#include <iostream>
#include <fstream>
#include <filesystem>
#include <string>
#include <sstream>
#include <vector>

#include <assert.h>

enum class Language
{
	Cpp,
	CSharp
};

struct Config
{
	bool generate_service = false;
	std::vector<std::filesystem::path> inputs;
	std::filesystem::path output_dir;
	std::filesystem::path depfile;
	Language language;
};

struct Context
{
	Context(const std::filesystem::path &i, const Config &c)
		: config(c), input(i), data_header_output((config.output_dir / input.stem()) += ".h"), cs_data_output((config.output_dir / input.stem()) += ".cs"), service_header_output((config.output_dir / input.stem()) += ".service.h"), service_cpp_output((config.output_dir / input.stem()) += ".service.cpp"), cs_service_output((config.output_dir / input.stem()) += ".service.cs")
	{
	}
	const Config &config;
	const std::filesystem::path input;
	const std::filesystem::path data_header_output;
	const std::filesystem::path service_header_output;
	const std::filesystem::path service_cpp_output;
	const std::filesystem::path cs_data_output;
	const std::filesystem::path cs_service_output;
	std::vector<std::filesystem::path> includes;
	std::vector<std::string> services;
	std::vector<std::string> data;
	std::vector<std::string> include_services;
	std::vector<std::string> include_data;
};

Config parse_arg(int argc, char **argv)
{
	assert(argc > 0);

	std::vector<std::string> args;

	Config config;

	for (int i = 1; i < argc; i++)
	{
		args.push_back(argv[i]);
	}

	for (int i = 0; i < args.size(); i++)
	{
		auto arg = args[i];
		if (arg == "--generate_service")
		{
			config.generate_service = true;
		}
		else if (arg == "--output_dir")
		{
			i += 1;
			config.output_dir = args[i];
		}
		else if (arg == "--depfile")
		{
			i += 1;
			config.depfile = args[i];
		}
		else if (arg == "--cpp")
		{
			config.language = Language::Cpp;
		}
		else if (arg == "--csharp")
		{
			config.language = Language::CSharp;
		}
		else
		{
			config.inputs.emplace_back(arg);
		}
	}

	assert(args.size() > 3);

	assert(std::filesystem::is_directory(config.output_dir) && "output_dir does not exist");

	return config;
}

const std::string WHITESPACE = " \n\r\t\f\v";
std::string ltrim(const std::string &s)
{
	size_t start = s.find_first_not_of(WHITESPACE);
	return (start == std::string::npos) ? "" : s.substr(start);
}

std::string rtrim(const std::string &s)
{
	size_t end = s.find_last_not_of(WHITESPACE);
	return (end == std::string::npos) ? "" : s.substr(0, end + 1);
}

std::string trim(const std::string &s)
{
	return rtrim(ltrim(s));
}

bool str_start_with(const std::string &mainStr, const std::string &toMatch)
{
	if (mainStr.find(toMatch) == 0)
		return true;
	else
		return false;
}

std::string convert_path(const std::filesystem::path &p)
{
	std::string tmp = p.string();
	std::stringstream result;
	for (char c : tmp)
	{
		if (c == '\\')
		{
			result << '/';
		}
		else
		{
			result << c;
		}
	}

	return result.str();
}

std::string extract_value(const std::string &line, const std::string &keyword)
{
	std::string r = line.substr(keyword.size());
	assert(r.size() > 0 && "value should not be empty");
	return r;
}

const std::string include_keyword = "include ";
const std::string data_keyword = "data ";
const std::string service_keyword = "service ";
const std::string comment_keyword = "#";

void parse_source(std::filesystem::path input, Context &context, bool is_include = false)
{

	std::ifstream file(input.string());
	assert(file.is_open() && "Cannot open the input file");
	context.includes.push_back(input);

	std::string line;
	while (std::getline(file, line))
	{
		line = trim(line);
		if (line.size() == 0)
		{
			continue;
		}

		if (str_start_with(line, include_keyword))
		{
			std::filesystem::path include_file = input.parent_path() / extract_value(line, include_keyword);
			parse_source(include_file, context, true);
		}
		else if (str_start_with(line, data_keyword))
		{
			if (is_include)
			{
				context.include_data.push_back(extract_value(line, data_keyword));
			}
			else
			{
				context.data.push_back(extract_value(line, data_keyword));
			}
		}
		else if (str_start_with(line, service_keyword))
		{
			assert(context.config.generate_service && "service parsing is disabled, enable it with \"--generate_service\"");
			if (is_include)
			{
				context.include_services.push_back(extract_value(line, service_keyword));
			}
			else
			{
				context.services.push_back(extract_value(line, service_keyword));
			}
		}
		else
		{
			assert(str_start_with(line, comment_keyword) && "Invalid keyword");
		}
	}
}

//
// command:
//     rpc_generator.exe --generate_service --depfile <depfile> --output_dir <output directory> input1 [input2 ...]
int main(int argc, char **argv)
{
	Config config = parse_arg(argc, argv);

	std::vector<Context> context_pool;
	for (auto &input : config.inputs)
	{
		assert(std::filesystem::exists(input) && "The input file does not exist");

		Context &context = context_pool.emplace_back(input, config);
		std::vector<std::filesystem::path> includes;
		parse_source(input, context);

		if (config.language == Language::Cpp)
		{
			std::ofstream file(context.data_header_output.c_str());
			assert(file.is_open() && "data_header_output cannot be open");

			file << "// generated by: rpc_generator.exe\n\n";
			for (auto &data : context.include_data)
			{
				file << "// data present in the includes:" << data << '\n';
			}
			file << '\n';
			file << "#pragma once\n";
			file << '\n';

			for (auto &data : context.data)
			{
				file << "struct " << data << " {\n";
				file << "};\n\n";
			}
		}
		if (config.language == Language::CSharp)
		{
			std::ofstream file(context.cs_data_output.c_str());
			assert(file.is_open() && "cs_data_header_output cannot be open");

			file << "// generated by: rpc_generator.exe\n\n";
			for (auto &data : context.include_data)
			{
				file << "// data present in the includes:" << data << '\n';
			}

			for (auto &data : context.data)
			{
				file << "public class " << data << " {\n";
				file << "}\n\n";
			}
		}
		if (config.language == Language::Cpp && config.generate_service)
		{
			std::ofstream header(context.service_header_output.c_str());
			std::ofstream cpp(context.service_cpp_output.c_str());
			assert(header.is_open() && "service_header_output cannot be open");
			assert(cpp.is_open() && "serice_cpp_output cannot be open");

			header << "// generated by: rpc_generator.exe\n\n";
			header << '\n';
			header << "#pragma once\n";
			header << '\n';
			cpp << "// generated by: rpc_generator.exe\n\n";
			cpp << "#include \"" << convert_path(context.service_header_output.filename()) << "\"\n\n";
			for (auto &service : context.include_services)
			{
				header << "// service present in the includes:" << service << '\n';
			}
			header << '\n';

			header << "static const char* ServiceInfo[] = {\n";
			for (auto &service : context.services)
			{
				header << "    \"" << service << "\",\n";
			}
			header << "};\n\n";

			for (auto &service : context.services)
			{
				header << "struct " << service << " {\n";
				header << "    static const char* getName();\n";
				header << "};\n\n";

				cpp << "const char* " << service << "::getName() {\n";
				cpp << "    return \"" << service << "\";\n";
				cpp << "};\n\n";
			}
		}
		if (config.language == Language::CSharp && config.generate_service) 
		{
			std::ofstream cs(context.cs_service_output.c_str());
			assert(cs.is_open() && "cs_serice_output cannot be open");

			cs << "// generated by: rpc_generator.exe\n\n";

			cs << "public class ServiceInfo {\n";
			cs << "  static public string[] GetServiceNames() {\n";
			cs << "    return new string[] {\n";
			for (auto &service : context.services)
			{
				cs << "        \"" << service << "\",\n";
			}
			cs << "    };\n";
			cs << "  }\n";
			cs << "};\n\n";

			for (auto &service : context.services)
			{
				cs << "public class " << service << " {\n";
				cs << "  static public string GetName() {\n";
				cs << "    return \"" << service << "\";\n";
				cs << "  }\n";
				cs << "};\n\n";
			}
		}
	}

	if (config.depfile.string().size() > 0)
	{
		std::ofstream file(config.depfile.c_str());
		assert(file.is_open() && "depfile cannot be open");

		for (auto &context : context_pool)
		{
			if (context.includes.size() > 0)
			{
				if (config.language == Language::Cpp)
				{
					file << convert_path(context.data_header_output) << ": \\\n";
				}
				else
				{
					file << convert_path(context.cs_data_output) << ": \\\n";
				}
				for (auto &include : context.includes)
				{
					file << "    " << convert_path(include) << " \\\n";
				}
				file << "\n";
			}
		}
	}

	return 0;
}