setlocal
echo off

REM The script purpose is to demonstrate the build with a bash script
REM Of course it will not support incremental build

REM SETTING

set MSVC_DIR=C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.16.27023
set WINSDK_VER=10.0.18362.0
set WINSDK_INCLUDE=C:\Program Files (x86)\Windows Kits\10\Include\%WINSDK_VER%
set WINSDK_LIB=C:\Program Files (x86)\Windows Kits\10\Lib\%WINSDK_VER%

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
set Path=%MSVC_DIR%\bin\Hostx64\x64;%Path%
set INCLUDE=%MSVC_DIR%\include;%WINSDK_INCLUDE%\ucrt
set LIB=%MSVC_DIR%\lib\x64;%WINSDK_LIB%\ucrt\x64;%WINSDK_LIB%\um\x64
set imd=%IMD_DIR%\cl_64
set out=%OUT_DIR%\cl_64
mkdir "%imd%" || goto :error
mkdir "%out%" || goto :error
cl.exe /c /EHsc /Fo"%imd%\HelloWorld.obj" src\HelloWorld.cpp || goto :error
link.exe /out:"%out%\HelloWorld.exe" "%imd%\HelloWorld.obj" || goto :error
endlocal

setlocal
set Path=%MSVC_DIR%\bin\Hostx86\x86;%Path%
set INCLUDE=%MSVC_DIR%\include;%WINSDK_INCLUDE%\ucrt
set LIB=%MSVC_DIR%\lib\x86;%WINSDK_LIB%\ucrt\x86;%WINSDK_LIB%\um\x86
set imd=%IMD_DIR%\cl_86
set out=%OUT_DIR%\cl_86
mkdir "%imd%" || goto :error
mkdir "%out%" || goto :error
cl.exe /c /EHsc /Fo"%imd%\HelloWorld.obj" src\HelloWorld.cpp || goto :error
link.exe /out:"%out%\HelloWorld.exe" "%imd%\HelloWorld.obj" || goto :error
endlocal

echo Build is success
popd
exit /b 0

:error
echo Build has failed
popd

exit /b %errorlevel%

