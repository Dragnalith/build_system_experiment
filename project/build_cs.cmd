@echo off
setlocal

REM The script purpose is to demonstrate the build with a bash script
REM Of course it will not support incremental build

REM SETTING
set MSBUILD=C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin\MSBuild.exe
set CSC=C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\MSBuild\15.0\Bin\Roslyn\csc.exe
set NET_FW=C:\Windows\Microsoft.NET\Framework64\v4.0.30319

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
set imd=%IMD_DIR%\CSharp
set out=%OUT_DIR%\CSharp
mkdir "%imd%" || goto :error
mkdir "%out%" || goto :error
echo Compile: MainWindow.xaml
"%MSBUILD%" /t:ResolveReferences;MarkupCompilePass1;MarkupCompilePass2 /p:XAMLInput=MainWindow.xaml /p:BAMLOutputDir=tmp src\hello_world_cs\tool_ui\compile_xaml.csproj
echo Compile: tool_ui.exe
"%CSC%" -nologo -lib:"%NET_FW%" -lib:"%NET_FW%\WPF" -reference:System.dll -reference:System.Xaml.dll -reference:WindowsBase.dll -reference:PresentationCore.dll -reference:PresentationFramework.dll -out:"%out%\tool_ui.exe" src\hello_world_cs\tool_ui\tmp\MainWindow.g.cs src\hello_world_cs\tool_ui\Program.cs src\hello_world_cs\tool_ui\MainWindow.xaml.cs src\hello_world_cs\tool_ui\Properties\AssemblyInfo.cs || goto :error
echo Compile: tool_lib.dll
"%CSC%" -nologo -target:library -out:"%out%\tool_lib.dll" src\hello_world_cs\tool_lib\Tool.cs src\hello_world_cs\tool_lib\Properties\AssemblyInfo.cs || goto :error
echo Compile: tool_cli.exe
"%CSC%" -nologo -lib:"%out%" -reference:tool_lib.dll -out:"%out%\tool_cli.exe" src\hello_world_cs\tool_cli\Program.cs src\hello_world_cs\tool_cli\Properties\AssemblyInfo.cs || goto :error
endlocal

echo Build is success
popd
exit /b 0

:error
echo Build has failed
popd

exit /b %errorlevel%

