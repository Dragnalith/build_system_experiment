#pragma once

#include <string>
namespace drgn
{

int getVersion();
const char* getName();
const char* getPlatformName();
std::string getComputerServiceList();

}