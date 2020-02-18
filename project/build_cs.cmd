@echo off
setlocal

REM The script purpose is to demonstrate the build with a bash script
REM Of course it will not support incremental build

REM SETTING
set ROSLYN_DIR=C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin\Roslyn

set BUILD_DIR=..\out\build-cmd
set IMD_DIR=%BUILD_DIR%\intermediate
set OUT_DIR=%BUILD_DIR%\out

REM START
pushd %~dp0

REM clean & create the build directory
rmdir /s /q "%BUILD_DIR%"
mkdir "%BUILD_DIR%"

REM start compilation

setlocal
set Path=%ROSLYN_DIR%;%Path%
set out=%OUT_DIR%\CSharp
mkdir "%out%" || goto :error
echo Compile: tool_lib.dll
csc.exe -nologo -target:library -out:"%out%\tool_lib.dll" src\hello_world_cs\tool_lib\Tool.cs src\hello_world_cs\tool_lib\Properties\AssemblyInfo.cs || goto :error
echo Compile: tool_cli.exe
csc.exe -nologo -lib:"%out%" -reference:tool_lib.dll -out:"%out%\tool_cli.exe" src\hello_world_cs\tool_cli\Program.cs src\hello_world_cs\tool_cli\Properties\AssemblyInfo.cs || goto :error
endlocal

echo Build is success
popd
exit /b 0

:error
echo Build has failed
popd

exit /b %errorlevel%

